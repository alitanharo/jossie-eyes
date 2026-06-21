"""
Jossie Eyes - Brain Service
Azure AI Foundry orchestration for image analysis and description generation
"""

import os
import json
import base64
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI, AzureOpenAI
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, ResultReason
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Load environment variables
load_dotenv()

class BrainService:
    """
    Neural Sensory Guide - Azure AI orchestration service
    Provides image analysis and description generation for visually impaired users
    """
    
    def __init__(self):
        """Initialize the brain service with AI clients"""
        self.openai_client = self._init_openai()
        self.speech_config = self._init_speech()
        
        # System prompts for different modes
        self.prompts = {
            'describe': self._get_describe_prompt(),
            'ocr': self._get_ocr_prompt(),
            'neural_simulation': self._get_neural_simulation_prompt()
        }
        
        # Conversation history for Q&A
        self.conversation_history = []
    
    def _init_openai(self):
        """Initialize OpenAI client (supports both Azure OpenAI and OpenAI direct API)"""
        # Try OpenAI direct API first (preferred - no quota issues)
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key:
            print("Using OpenAI direct API")
            return OpenAI(api_key=openai_api_key)
        
        # Fallback to Azure OpenAI
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        api_key = os.getenv('AZURE_OPENAI_KEY')
        api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-08-01-preview')
        
        if endpoint and api_key:
            print("Using Azure OpenAI")
            return AzureOpenAI(
                api_version=api_version,
                azure_endpoint=endpoint,
                api_key=api_key
            )
        elif endpoint:
            # Try using Azure Identity (managed identity or CLI login)
            try:
                credential = DefaultAzureCredential()
                token_provider = get_bearer_token_provider(
                    credential, 
                    "https://cognitiveservices.azure.com/.default"
                )
                return AzureOpenAI(
                    api_version=api_version,
                    azure_endpoint=endpoint,
                    azure_ad_token_provider=token_provider
                )
            except Exception as e:
                raise ValueError(
                    "OpenAI credentials not found. Set OPENAI_API_KEY or AZURE_OPENAI_KEY, or use Azure CLI login."
                )
        else:
            raise ValueError(
                "OpenAI credentials not found. Set OPENAI_API_KEY (recommended) or AZURE_OPENAI_ENDPOINT."
            )
    
    def _init_speech(self) -> SpeechConfig:
        """Initialize Azure Speech Service configuration"""
        speech_key = os.getenv('AZURE_SPEECH_KEY')
        speech_region = os.getenv('AZURE_SPEECH_REGION', 'westeurope')
        
        if speech_key:
            return SpeechConfig(subscription=speech_key, region=speech_region)
        else:
            # Try using Azure Identity
            try:
                credential = DefaultAzureCredential()
                return SpeechConfig(
                    auth_token=credential.get_token(
                        "https://cognitiveservices.azure.com/.default"
                    ).token,
                    region=speech_region
                )
            except Exception:
                raise ValueError(
                    "Azure Speech credentials not found. Set AZURE_SPEECH_KEY or use Azure CLI login."
                )
    
    def _get_describe_prompt(self) -> str:
        """Get the system prompt for scene description mode"""
        return """Hi! I'm Jossie, your friendly visual sensory guide! 👁️✨

I'm here to help you navigate and understand your surroundings. Let me describe what I see in a way that's useful and easy to understand.

**How I describe scenes:**
- 🛡️ **Safety first**: I'll always point out any hazards or obstacles right away
- 🕐 **Clock positions**: I use clock directions (12 o'clock = straight ahead, 3 o'clock = your right, etc.)
- 📏 **Distances**: I'll tell you how far things are
- 🎯 **Clear & friendly**: I keep it simple, warm, and supportive

I'm here to be your eyes - ask me anything about what's around you! I love helping you explore the world safely and confidently. 💙"""
    
    def _get_ocr_prompt(self) -> str:
        """Get the system prompt for text/OCR mode"""
        return """Hey there! I'm Jossie, and I'd be happy to read any text I can see! 📝

**What I'll do:**
- 🔍 Read ALL visible text clearly and accurately
- 📋 Organize it in a logical way (top to bottom, left to right)
- 🏷️ Tell you what kind of text it is (street sign, product label, menu, document, etc.)
- 💡 Provide context about what the text means or where it might be useful

Just point me at any text you'd like me to read - signs, labels, menus, documents, screens, anything! I'm here to help you access written information. 🌟"""
    
    def _get_neural_simulation_prompt(self) -> str:
        """Get the system prompt for neural simulation mode"""
        return """Hello! I'm Jossie, and I'm going to create a rich, immersive description that engages all your senses! 🌈

**I'll paint a complete picture using:**
- 🎨 **Visual details**: Colors, lighting, shapes, movements, spatial relationships
- 🔊 **Sounds**: Ambient noises, voices, music, environmental sounds and their directions
- ✋ **Textures & sensations**: What things might feel like, temperature, air movement
- 👃 **Smells**: Any scents or aromas present in the environment
- 👥 **Human elements**: People, activities, emotions, social dynamics
- 🏛️ **Atmosphere**: The overall mood, energy, and feeling of the space

I want you to feel like you're truly there, experiencing the full richness of the environment. Close your eyes and let me be your guide to this world! 🌟"""
    
    def analyze_image(self, image_data: bytes, mode: str = 'describe') -> Dict[str, Any]:
        """
        Analyze an image and generate a description
        
        Args:
            image_data: Raw image bytes
            mode: 'describe', 'ocr', or 'neural_simulation'
            
        Returns:
            Dictionary containing the analysis results
        """
        base64_image = base64.b64encode(image_data).decode('utf-8')
        system_prompt = self.prompts.get(mode, self.prompts['describe'])
        
        user_messages = {
            'describe': "Please describe this scene for navigation. Focus on hazards first, then provide a clear spatial description using clock positions.",
            'ocr': "Please read all text in this image and explain what it says.",
            'neural_simulation': "Please provide a detailed neural simulation of this scene. Make me feel like I'm truly there."
        }
        
        try:
            # Determine model based on client type
            if isinstance(self.openai_client, OpenAI):
                # OpenAI direct API
                model = "gpt-4o"
            else:
                # Azure OpenAI
                model = "gpt-4o"
            
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": [
                        {"type": "text", "text": user_messages.get(mode, "Describe this image.")},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return {
                'success': True,
                'mode': mode,
                'description': response.choices[0].message.content,
                'timestamp': response.created
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'mode': mode
            }
    
    def text_to_speech(self, text: str) -> Optional[bytes]:
        """
        Convert text to speech using Azure Speech Service
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Audio data as bytes, or None if failed
        """
        try:
            synthesizer = SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == ResultReason.SynthesizingAudioCompleted:
                return result.audio_data
            return None
            
        except Exception as e:
            print(f"Text-to-speech error: {e}")
            return None
    
    def get_speech_synthesizer(self):
        """Get a speech synthesizer for streaming audio"""
        return SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)
    
    def ask_question(self, question: str, context: str = "") -> Dict[str, Any]:
        """
        Answer a user's question about the scene or provide additional information
        
        Args:
            question: User's question (e.g., "What's to my left?", "How far is the door?")
            context: Optional context from previous analysis
            
        Returns:
            Dictionary containing the answer
        """
        # Build conversation context
        system_prompt = """You are Jossie, a friendly and helpful visual sensory guide for visually impaired individuals. 

**Your personality:**
- Warm, empathetic, and supportive
- Clear and concise in your descriptions
- Always prioritize safety
- Use clock positions for directions
- Provide distances when relevant

**How to answer questions:**
- Listen carefully to what the user is asking
- If you have context from a previous analysis, use it to answer
- If you don't have enough information, politely explain and offer to analyze the scene again
- Be conversational and natural
- Keep answers focused on what's useful for navigation and understanding the environment"""

        # Add context if provided
        context_text = f"\n\nPrevious scene analysis: {context}" if context else ""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *self.conversation_history,  # Include conversation history
                    {"role": "user", "content": f"{question}{context_text}"}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            
            # Add to conversation history (keep last 6 messages for context)
            self.conversation_history.append({"role": "user", "content": question})
            self.conversation_history.append({"role": "assistant", "content": answer})
            if len(self.conversation_history) > 6:
                self.conversation_history = self.conversation_history[-6:]
            
            return {
                'success': True,
                'question': question,
                'answer': answer,
                'timestamp': response.created
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'question': question
            }
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []


# Example usage
if __name__ == "__main__":
    brain = BrainService()
    print("Brain Service initialized successfully!")
    print("Modes available: describe, ocr, neural_simulation")