# SkinCareRecommendationSystem

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies and Techniques](#technologies-and-techniques)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Evaluation Strategy](#evaluation-strategy)
8. [Future Work](#future-work)
9. [Contributing](#contributing)
10. [License](#license)

---

## Project Overview

In today's world, where finding suitable skincare products can be challenging due to countless options and complex ingredient lists, our **Interactive Skincare Recommendation System** aims to simplify this process. This system engages users through a chat-based interface to understand their skin types, concerns, and preferences. By analyzing images of the user’s skin and understanding personal skincare goals, the system recommends personalized skincare routines and products, helping users make informed decisions without overwhelming them.

## Features

1. **Interactive Chatbot**: Guides users through skin assessment, skincare queries, and personalized recommendations.
2. **Image-Based Analysis**: Uses convolutional neural networks to analyze skin images for acne detection and severity analysis.
3. **Personalized Recommendations**: Based on collaborative filtering and user similarity to suggest skincare routines and products.
4. **Data Privacy**: Images uploaded by users are securely deleted after analysis to ensure privacy.
5. **Continuous Learning**: Refines recommendations based on user feedback, improving over time.

## Technologies and Techniques

### Frontend
- **Frameworks**: [React.js](https://reactjs.org/) or [Vue.js](https://vuejs.org/) for the user interface.
- **Image Uploading**: Allows users to upload skin images for analysis.

### Backend
- **Natural Language Processing (NLP)**: Pretrained models (e.g., BERT, SpaCy) fine-tuned with [RASA](https://rasa.com/) for intent recognition and entity extraction.
- **Computer Vision**: A convolutional neural network, such as MobileNet, for image analysis to detect acne and classify its severity.
- **Recommendation Engine**: Collaborative filtering based on user-item interaction data to recommend products suited to users' skin types and concerns.

### Databases
- User and product data storage to facilitate the collaborative filtering process.
  
## Installation

### Prerequisites
- **Node.js** and **npm** for frontend setup
- **Python 3.8+** for backend and machine learning models
- **RASA** for natural language processing tasks
- **TensorFlow or PyTorch** for the CNN-based image analysis model

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/skincare-recommendation-system.git
   cd skincare-recommendation-system
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **NLP Setup**:
   - Download RASA pretrained models and train the model for intent and entity extraction.
   - Start the RASA server:
     ```bash
     rasa run --enable-api
     ```

5. **Run the Project**:
   - Ensure both frontend and backend are running to test the complete system.

## Usage

- **User Login**: Log in to the platform to start the skincare journey.
- **Chat with the Bot**: Interact with the bot to enter skincare concerns, preferences, and upload skin images.
- **Receive Recommendations**: Based on inputs, the bot provides a tailored skincare routine and product suggestions.
- **Refinement**: The system learns from user feedback, enhancing personalization over time.

## Project Structure

```plaintext
├── frontend/                # Contains React or Vue.js frontend
├── backend/                 # Backend server with REST API
├── models/                  # Machine learning models for NLP and image analysis
├── rasa/                    # RASA for intent and entity recognition
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
```

## Evaluation Strategy

### 1. **Intent Recognition**:
   - Measures the agent’s ability to capture user intent.
   - Metrics: Accuracy, Precision, Recall, and F1 Score.
   - Evaluation: Compares predicted intent to actual intent using confusion matrix.

### 2. **Entity Recognition**:
   - Extracts key information such as skin type, concerns, preferred ingredients.
   - Metrics: Accuracy, Precision, Recall, and F1 Score.
   - Evaluation: Confusion matrix to assess performance in extracting specific user details.

### 3. **First Response Time (FRT)**:
   - Measures the time taken by the bot to respond to the user’s initial query.

### 4. **Image Classification Performance**:
   - For acne severity classification, a confusion matrix will be used to evaluate:
     - True Positives, False Positives, True Negatives, False Negatives.
   - Metrics: Accuracy, Precision, Recall, and F1 Score.

## Future Work

- **Extended Skin Conditions**: Add support for detecting other skin conditions beyond acne.
- **Enhanced Collaborative Filtering**: Incorporate neural collaborative filtering to improve recommendation accuracy.
- **Integration with External Databases**: Directly retrieve product information from third-party databases for up-to-date recommendations.



---

Feel free to reach out for any queries or discussions on potential improvements.
