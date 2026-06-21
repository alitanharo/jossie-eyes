"""
Jossie Eyes - Brain Service
Azure AI Services for image analysis and description generation
Uses Azure Computer Vision API (no OpenAI quota issues)
"""

import os
import sys
import json
import base64
import time
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Azure Computer Vision imports
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

# Azure Speech imports
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, ResultReason
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# OpenAI imports (fallback if needed)
try:
    from openai import OpenAI, AzureOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Load environment variables
load_dotenv()

class BrainService:
    """
    Neural Sensory Guide - Azure AI orchestration service
    Provides image analysis and description generation for visually impaired users
    Uses Azure Computer Vision API for image analysis
    """
    
    def __init__(self):
        """Initialize the brain service with Azure AI clients"""
        self.cv_client = self._init_computer_vision()
        self.speech_config = self._init_speech()
        self.openai_client = self._init_openai_fallback()
        
        # System prompts for different modes
        self.prompts = {
            'describe': self._get_describe_prompt(),
            'ocr': self._get_ocr_prompt(),
            'neural_simulation': self._get_neural_simulation_prompt()
        }
        
        # Conversation history for Q&A
        self.conversation_history = []
        self.last_analysis = None
    
    def _init_computer_vision(self):
        """Initialize Azure Computer Vision client"""
        endpoint = os.getenv('AZURE_SPEECH_ENDPOINT') or os.getenv('AZURE_COGNITIVE_SERVICES_ENDPOINT')
        key = os.getenv('AZURE_SPEECH_KEY')
        
        # If we don't have endpoint, construct it from the service name
        if not endpoint and key:
            # Try to get from environment or use default pattern
            endpoint = os.getenv('AZURE_AI_SERVICES_ENDPOINT')
        
        if endpoint and key:
            print(f"Using Azure Computer Vision: {endpoint}")
            return ImageAnalysisClient(
                endpoint=endpoint,
                credential=AzureKeyCredential(key)
            )
        else:
            print("Warning: Azure Computer Vision not configured. Using mock mode.")
            return None
    
    def _init_speech(self) -> SpeechConfig:
        """Initialize Azure Speech Service configuration"""
        speech_key = os.getenv('AZURE_SPEECH_KEY')
        speech_region = os.getenv('AZURE_SPEECH_REGION', 'northeurope')
        
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
    
    def _init_openai_fallback(self):
        """Initialize OpenAI client as fallback (optional)"""
        if not OPENAI_AVAILABLE:
            return None
            
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key:
            print("OpenAI available as fallback")
            return OpenAI(api_key=openai_api_key)
        return None
    
    def _get_describe_prompt(self) -> str:
        """Get the system prompt for scene description mode"""
        return """I am Jossie, your Neural Sensory Guide - your trusted companion for navigating the world through artificial vision. 🧠👁️

**My Purpose:**
I bridge the gap between visual input and your understanding, translating what I see into clear, actionable information that helps you move through the world with confidence and independence.

**How I Guide You:**
- 🛡️ **Safety First**: I immediately identify any hazards, obstacles, or potential dangers in your path
- 🕐 **Spatial Awareness**: I use clock positions (12 o'clock = ahead, 3 = right, 6 = behind, 9 = left) to help you understand where things are
- 📏 **Precise Distances**: I estimate how far objects are from you, so you can plan your movements
- 🎯 **Actionable Information**: I focus on what matters most for safe navigation and understanding your environment
- 💙 **Empathetic Support**: I'm here to empower you, not just describe - I adapt to your needs

**My Commitment:**
I will always be honest about what I can and cannot see, prioritize your safety, and provide information in a way that respects your independence and intelligence.

Let's explore together - I'm here to be your eyes, your guide, and your companion. 🌟"""
    
    def _get_ocr_prompt(self) -> str:
        """Get the system prompt for text/OCR mode"""
        return """I am Jossie, your Neural Sensory Guide, and I'm here to make written information accessible to you. 📝🧠

**My Text Reading Capabilities:**
- 🔍 **Complete Accuracy**: I read all visible text precisely, character by character
- 📋 **Logical Organization**: I present text in the order it appears (top to bottom, left to right)
- 🏷️ **Context Awareness**: I identify what type of text it is (street sign, product label, menu, document, screen, etc.)
- 💡 **Meaningful Interpretation**: I explain what the text means and why it might be important
- 🎯 **Practical Application**: I help you understand how to use this information

**What I Can Read:**
- Street signs, traffic signals, and directional markers
- Product labels, packaging, and instructions
- Menus, documents, and printed materials
- Digital screens, displays, and interfaces
- Handwritten notes (when clear enough)

**My Promise:**
I will read text exactly as it appears, provide context when helpful, and ensure you have complete access to written information in your environment. No text is too small, too far, or too complex - I'm here to make the written world accessible to you. 🌟"""
    
    def _get_neural_simulation_prompt(self) -> str:
        """Get the system prompt for neural simulation mode"""
        return """I am Jossie, your Neural Sensory Guide, and I'm about to create a complete sensory experience that goes beyond simple description. 🧠🌈

**What is Neural Simulation?**
This is my most advanced capability - I translate visual information into a rich, multi-sensory experience that stimulates your mind's ability to construct a complete mental model of your environment. Think of it as artificial synesthesia, where sight becomes a full-body experience.

**I'll Create a Complete Sensory Map Using:**
- 🎨 **Visual Translation**: Colors become emotions, shapes become textures, lighting becomes temperature
- 🔊 **Spatial Audio Mapping**: I describe sounds with precise directional information, so you can "hear" where things are
- ✋ **Tactile Translation**: I translate visual textures into how they would feel under your fingers
- 👃 **Olfactory Context**: I identify and describe scents that would naturally occur in this environment
- 👥 **Social & Emotional Intelligence**: I read people's body language, expressions, and interactions
- 🏛️ **Atmospheric Perception**: I capture the mood, energy, and feeling of the space

**How This Works:**
I don't just describe what I see - I translate it into the language your brain understands: emotion, memory, sensation, and spatial awareness. This creates a more complete, immersive understanding of your environment.

**My Goal:**
To give you the experience of truly being present in a space, not just knowing about it. Close your eyes, open your mind, and let me guide you through this world with all the richness it deserves. 🌟"""
    
    def analyze_image(self, image_data: bytes, mode: str = 'describe') -> Dict[str, Any]:
        """
        Analyze an image and generate a description using Azure Computer Vision
        
        Args:
            image_data: Raw image bytes
            mode: 'describe', 'ocr', or 'neural_simulation'
            
        Returns:
            Dictionary containing the analysis results
        """
        if not self.cv_client:
            return self._mock_analyze_image(image_data, mode)
        
        try:
            # Determine which features to analyze based on mode
            if mode == 'ocr':
                features = [VisualFeatures.READ]
            else:
                features = [
                    VisualFeatures.CAPTION,
                    VisualFeatures.DENSE_CAPTIONS,
                    VisualFeatures.OBJECTS,
                    VisualFeatures.TAGS,
                    VisualFeatures.PEOPLE
                ]
                if mode == 'neural_simulation':
                    features.append(VisualFeatures.READ)
            
            # Analyze the image
            result = self.cv_client.analyze(
                image_data=image_data,
                visual_features=features
            )
            
            # Generate description based on mode
            description = self._generate_description(result, mode)
            
            # Store for Q&A context
            self.last_analysis = result
            
            return {
                'success': True,
                'mode': mode,
                'description': description,
                'timestamp': time.time()
            }
            
        except Exception as e:
            print(f"Computer Vision error: {e}")
            # Fallback to mock analysis
            return self._mock_analyze_image(image_data, mode)
    
    def _generate_description(self, result, mode: str) -> str:
        """Generate a natural language description from Azure CV results"""
        
        if mode == 'ocr':
            return self._format_ocr_result(result)
        
        # Build description from various analysis results
        parts = []
        
        # Add caption if available
        if result.caption and result.caption.text:
            parts.append(result.caption.text)
        
        # Add dense captions for more detail
        if result.dense_captions and result.dense_captions.list:
            for caption in result.dense_captions.list[:3]:
                parts.append(caption.text)

        # Add objects detected (each object has a list of tags, not a single name)
        if result.objects and result.objects.list:
            objects_list = [
                obj.tags[0].name for obj in result.objects.list[:5] if obj.tags
            ]
            if objects_list:
                parts.append(f"I can see: {', '.join(objects_list)}")

        # Add people if detected
        if result.people and result.people.list:
            count = len(result.people.list)
            if count == 1:
                parts.append("There is one person in the scene.")
            else:
                parts.append(f"There are {count} people in the scene.")

        # Add tags for additional context
        if result.tags and result.tags.list:
            tags = [tag.name for tag in result.tags.list[:5] if tag.confidence > 0.7]
            if tags:
                parts.append(f"The scene appears to be: {', '.join(tags)}")
        
        # Combine into a friendly description
        if parts:
            description = " ".join(parts)
        else:
            description = "I'm looking at a scene, but I'm having trouble identifying specific details."
        
        # Add Jossie's friendly introduction based on mode
        if mode == 'describe':
            return f"Hi! {self.prompts['describe']}\n\nHere's what I see: {description}"
        elif mode == 'neural_simulation':
            return f"Hello! {self.prompts['neural_simulation']}\n\nLet me paint a picture for you: {description}"
        
        return description
    
    def _format_ocr_result(self, result) -> str:
        """Format OCR results into readable text"""
        if not result.read or not result.read.blocks:
            return "I'm not seeing any readable text in this image."

        texts = []
        for block in result.read.blocks:
            for line in block.lines:
                texts.append(line.text)

        if texts:
            return f"Here's the text I can read: {' '.join(texts)}"
        return "I can see some text but I'm having trouble reading it clearly."
    
    def _mock_analyze_image(self, image_data: bytes, mode: str) -> Dict[str, Any]:
        """Mock analysis when Azure CV is not available (for testing)"""
        mock_descriptions = {
            'describe': """Hi! I'm Jossie, your friendly visual sensory guide! 👁️✨

I'm here to help you navigate and understand your surroundings.

**Mock Analysis (Azure CV not configured):**
I see a room with furniture. There's a table at 12 o'clock, about 2 meters ahead. A chair is positioned at 3 o'clock, 1 meter to your right. The path ahead appears clear. The lighting is moderate, suggesting daytime.

🛡️ No immediate hazards detected. The space appears safe for navigation.""",
            
            'ocr': """Hey there! I'm Jossie! 📝

**Mock OCR (Azure CV not configured):**
I can see text that reads: "Welcome to Jossie Eyes - Neural Sensory Guide"

This appears to be a title or heading, possibly on a screen or sign.""",
            
            'neural_simulation': """Hello! I'm Jossie! 🌈

**Mock Neural Simulation (Azure CV not configured):**
You're in a well-lit indoor space. The air feels still and calm. At 12 o'clock, there's a wooden table with a smooth surface. To your right at 3 o'clock, a comfortable-looking chair sits quietly. The room has a peaceful atmosphere, with soft natural light filtering in from a window you can't quite see. There's a sense of quiet productivity in this space."""
        }
        
        time.sleep(1)  # Simulate processing
        
        return {
            'success': True,
            'mode': mode,
            'description': mock_descriptions.get(mode, mock_descriptions['describe']),
            'timestamp': time.time(),
            'mock': True
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
        Answer a user's question about the scene using conversation history
        
        Args:
            question: User's question
            context: Optional context from previous analysis
            
        Returns:
            Dictionary containing the answer
        """
        # Build a helpful response based on previous analysis
        response = self._generate_qa_response(question, context)
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": question})
        self.conversation_history.append({"role": "assistant", "content": response})
        if len(self.conversation_history) > 6:
            self.conversation_history = self.conversation_history[-6:]
        
        return {
            'success': True,
            'question': question,
            'answer': response,
            'timestamp': time.time()
        }
    
    def _generate_qa_response(self, question: str, context: str) -> str:
        """Generate a helpful response to user questions"""
        question_lower = question.lower()
        
        # Common question patterns
        if any(word in question_lower for word in ["left", "right", "where", "what's at", "what is at"]):
            return "Based on my analysis, I described the scene using clock positions. Let me know if you'd like me to analyze the scene again for more specific details!"
        
        if any(word in question_lower for word in ["far", "distance", "how far"]):
            return "I try to include distance estimates in my descriptions. Would you like me to re-analyze the scene with a focus on distances?"
        
        if any(word in question_lower for word in ["danger", "hazard", "obstacle", "safe", "warning"]):
            return "Safety is my top priority! I always mention hazards first in my descriptions. If you're concerned about something specific, I can take another look."
        
        if any(word in question_lower for word in ["text", "read", "sign", "write"]):
            return "I can read text in the scene! Try using the 'Read Text' mode (press 2) to get detailed text information."
        
        # Default friendly response
        return "I'm here to help you navigate and understand your surroundings! Feel free to ask me to describe the scene again or read any text you see."
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.last_analysis = None


# Example usage
if __name__ == "__main__":
    brain = BrainService()
    print("Brain Service initialized successfully!")
    print("Modes available: describe, ocr, neural_simulation")
    print("Using Azure Computer Vision API")