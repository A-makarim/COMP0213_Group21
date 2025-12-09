"""
AI-Powered Voice Assistant with Google Gemini
Answers questions about grasp planning data with intelligent insights
"""

import os
import sys
import pandas as pd
import pyttsx3
import speech_recognition as sr
import json
from pathlib import Path

# Gemini API
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("WARNING: google-generativeai not installed. Run: pip install google-generativeai")


class GeminiVoiceAssistant:
    """AI-powered assistant using Google Gemini for intelligent responses"""
    
    def __init__(self, api_key=None):
        """Initialize with Gemini API key"""
        
        # Text-to-Speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.9)
        
        # Speech Recognition
        self.recognizer = sr.Recognizer()
        self.speech_available = False
        
        try:
            self.microphone = sr.Microphone()
            print("Calibrating microphone...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.speech_available = True
            print("Microphone ready")
        except Exception as e:
            print(f"WARNING: Microphone not available: {e}")
            print("Keyboard mode will be used")
        
        # Initialize Gemini
        self.gemini_model = None
        self.api_key = api_key
        
        if GEMINI_AVAILABLE and api_key:
            try:
                genai.configure(api_key=api_key)
                # Try multiple model names for compatibility (Gemini 2.5 models)
                try:
                    self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                    print("Gemini AI connected (gemini-2.5-flash)")
                except:
                    try:
                        self.gemini_model = genai.GenerativeModel('gemini-flash-latest')
                        print("Gemini AI connected (gemini-flash-latest)")
                    except:
                        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
                        print("Gemini AI connected (gemini-2.0-flash)")
            except Exception as e:
                print(f"WARNING: Gemini initialization failed: {e}")
                print("INFO: Try: gemini-2.5-flash, gemini-flash-latest, or gemini-2.0-flash")
        elif not GEMINI_AVAILABLE:
            print("WARNING: Install google-generativeai: pip install google-generativeai")
        
        # Data files
        self.data_files = {
            'pr2_cuboid': 'data/updated_grasp_data_pr2_cuboid_with_predictions.csv',
            'pr2_cylinder': 'data/updated_grasp_data_pr2_cylinder_with_predictions.csv',
            'sdh_cuboid': 'data/updated_grasp_data_sdh_cuboid_with_predictions.csv',
            'sdh_cylinder': 'data/updated_grasp_data_sdh_cylinder_with_predictions.csv'
        }
        
        # Load all data
        self.data = {}
        self.load_all_data()
        
        self.running = True
    
    def load_all_data(self):
        """Load all CSV files into memory"""
        print("\nLoading data files...")
        
        for key, filepath in self.data_files.items():
            if os.path.exists(filepath):
                try:
                    self.data[key] = pd.read_csv(filepath)
                    print(f"Loaded {key}: {len(self.data[key])} samples")
                except Exception as e:
                    print(f"ERROR: Error loading {key}: {e}")
        
        print(f"\nTotal datasets loaded: {len(self.data)}\n")
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"\nAI: {text}\n")
        
        try:
            # For very long text, TTS can have issues - split into chunks
            max_chunk_size = 500  # characters
            
            if len(text) > max_chunk_size:
                # Split by sentences for more natural breaks
                sentences = text.replace('\n\n', '. ').replace('\n', ' ').split('. ')
                
                current_chunk = ""
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) < max_chunk_size:
                        current_chunk += sentence + ". "
                    else:
                        if current_chunk:
                            self.tts_engine.say(current_chunk)
                            self.tts_engine.runAndWait()
                        current_chunk = sentence + ". "
                
                # Speak the last chunk
                if current_chunk:
                    self.tts_engine.say(current_chunk)
                    self.tts_engine.runAndWait()
            else:
                # Short text - speak directly
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            print("Speech completed")
        except Exception as e:
            print(f"WARNING: TTS error: {e}")
    
    def listen(self, timeout=10):
        """Listen for voice input"""
        if not self.speech_available:
            print("ERROR: Voice input not available!")
            return None
        
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
            
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("Timeout - please speak again")
            return None
        except sr.UnknownValueError:
            print("ERROR: Could not understand - please speak again")
            return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None
    
    def get_input(self):
        """Get user input via voice only"""
        while True:
            result = self.listen()
            if result:
                return result
            # Keep trying until we get valid input
            print("Let's try again...")
    
    def create_data_context(self, question):
        """Create context from data for Gemini"""
        
        context = "# Grasp Planning Project Data\n\n"
        context += "You are an AI assistant helping analyze robotic grasp planning data.\n\n"
        
        # Add data summaries
        for key, df in self.data.items():
            gripper, obj = key.split('_')
            
            context += f"\n## {gripper.upper()} Gripper + {obj.capitalize()} Object\n"
            context += f"- Total samples: {len(df)}\n"
            
            if 'Success' in df.columns:
                success_count = df['Success'].sum()
                success_rate = (success_count / len(df)) * 100
                context += f"- Successful grasps: {success_count}\n"
                context += f"- Success rate: {success_rate:.1f}%\n"
            
            if 'Delta Z' in df.columns:
                context += f"- Average lift: {df['Delta Z'].mean():.3f}m\n"
                context += f"- Max lift: {df['Delta Z'].max():.3f}m\n"
                context += f"- Min lift: {df['Delta Z'].min():.3f}m\n"
            
            if 'Predicted Success' in df.columns:
                pred_count = df['Predicted Success'].sum()
                context += f"- ML Predictions: {pred_count} successful\n"
        
        context += f"\n\n# User Question:\n{question}\n\n"
        context += "Provide a clear, concise answer with insights and data-driven explanations."
        
        return context
    
    def ask_gemini(self, question):
        """Ask Gemini AI a question with data context"""
        
        if not self.gemini_model:
            return "Gemini AI is not available. Please provide an API key."
        
        try:
            # Create context with data
            context = self.create_data_context(question)
            
            # Generate response
            print("Thinking...")
            response = self.gemini_model.generate_content(context)
            
            return response.text
            
        except Exception as e:
            error_msg = str(e)
            
            # Provide helpful error messages
            if "404" in error_msg or "not found" in error_msg:
                return (
                    "The Gemini model is not available. This might be due to:\n"
                    "1. Your API key needs Gemini 1.5 access\n"
                    "2. The model name has changed\n"
                    "3. API quota exceeded\n\n"
                    "Try getting a new API key from: https://makersuite.google.com/app/apikey\n"
                    f"Technical error: {error_msg}"
                )
            elif "quota" in error_msg.lower():
                return (
                    "API quota exceeded. Please check your Google AI Studio account at:\n"
                    "https://makersuite.google.com/\n"
                    f"Error: {error_msg}"
                )
            else:
                return f"Error getting AI response: {error_msg}"
    
    def show_data_summary(self):
        """Show quick data summary"""
        summary = "Here's a summary of all available data. "
        
        for key, df in self.data.items():
            gripper, obj = key.split('_')
            summary += f"\n{gripper.upper()} with {obj}: {len(df)} samples. "
            
            if 'Success' in df.columns:
                success_rate = (df['Success'].sum() / len(df)) * 100
                summary += f"Success rate: {success_rate:.1f} percent. "
        
        self.speak(summary)
        
        # Print detailed table
        print("\n" + "="*80)
        print("DATA SUMMARY")
        print("="*80)
        
        for key, df in self.data.items():
            gripper, obj = key.split('_')
            print(f"\n{gripper.upper()} + {obj.capitalize()}")
            print(f"  Samples: {len(df)}")
            
            if 'Success' in df.columns:
                success_count = df['Success'].sum()
                success_rate = (success_count / len(df)) * 100
                print(f"  Success: {success_count}/{len(df)} ({success_rate:.1f}%)")
            
            if 'Delta Z' in df.columns:
                print(f"  Lift: avg={df['Delta Z'].mean():.3f}m, max={df['Delta Z'].max():.3f}m")
        
        print("="*80 + "\n")
    
    def run(self):
        """Main assistant loop"""
        
        print("\n" + "="*80)
        print("  AI-POWERED VOICE ASSISTANT WITH GEMINI")
        print("  Ask questions about your grasp planning data")
        print("="*80 + "\n")
        
        if not self.gemini_model:
            self.speak("Warning: Gemini AI is not configured. I can still show data summaries.")
        
        if not self.speech_available:
            print("ERROR: Voice input is not available!")
            print("Please check your microphone and PyAudio installation.")
            return
        
        # Show help
        self.speak("Welcome to the voice assistant. You can ask questions about your grasp data.")
        
        print("\n" + "="*80)
        print("EXAMPLE QUESTIONS:")
        print("="*80)
        print("- Which gripper has the best success rate?")
        print("- Why does SDH perform worse than PR2?")
        print("- What's the average lift height for each configuration?")
        print("- How accurate are the machine learning predictions?")
        print("- Compare PR2 and SDH performance on cylinders")
        print("- Show me data summary")
        print("- Say 'exit' or 'quit' to stop")
        print("="*80 + "\n")
        
        # Main loop
        while self.running:
            try:
                # Get question via voice
                self.speak("What would you like to know?")
                question = self.get_input()
                
                if not question:
                    continue
                
                question_lower = question.lower()
                
                # Check for exit
                if any(word in question_lower for word in ['exit', 'quit', 'bye', 'goodbye', 'stop']):
                    self.speak("Goodbye! Have a great day.")
                    break
                
                # Check for summary request
                elif any(word in question_lower for word in ['summary', 'show data', 'overview']):
                    self.show_data_summary()
                
                # Ask Gemini
                elif self.gemini_model:
                    answer = self.ask_gemini(question)
                    self.speak(answer)
                
                else:
                    self.speak("I can show data summaries, but I need a Gemini API key for intelligent answers.")
                    self.show_data_summary()
                
            except KeyboardInterrupt:
                self.speak("Interrupted. Exiting.")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                self.speak("An error occurred. Please try again.")


def setup_api_key():
    """Help user setup API key"""
    
    print("\n" + "="*80)
    print("  GEMINI API KEY SETUP")
    print("="*80 + "\n")
    
    print("To use AI-powered responses, you need a Google Gemini API key.")
    print("\nHow to get one:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the API key\n")
    
    api_key = input("Paste your Gemini API key here (or press Enter to skip): ").strip()
    
    if api_key:
        # Save to config file
        config_file = Path("gemini_config.json")
        config = {"api_key": api_key}
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f)
            print("API key saved to gemini_config.json")
            return api_key
        except Exception as e:
            print(f"WARNING: Could not save key: {e}")
            return api_key
    
    return None


def load_api_key():
    """Load API key from config file"""
    config_file = Path("gemini_config.json")
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get("api_key")
        except Exception as e:
            print(f"WARNING: Could not load config: {e}")
    
    return None


def main():
    """Main entry point"""
    
    # Check if google-generativeai is installed
    if not GEMINI_AVAILABLE:
        print("\n" + "="*80)
        print("  WARNING: MISSING DEPENDENCY")
        print("="*80)
        print("\nTo use Gemini AI, install the package:")
        print("\n  pip install google-generativeai")
        print("\nContinuing without AI features...\n")
        
        response = input("Press Enter to continue or Ctrl+C to exit: ")
    
    # Try to load existing API key
    api_key = load_api_key()
    
    if not api_key:
        api_key = setup_api_key()
    else:
        print(f"Using saved API key: {api_key[:10]}...")
    
    # Create and run assistant
    try:
        assistant = GeminiVoiceAssistant(api_key=api_key)
        assistant.run()
    except Exception as e:
        print(f"\nERROR: Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
