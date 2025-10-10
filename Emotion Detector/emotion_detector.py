{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "4d284502-d8c7-42a9-a800-9a11103cd2bb",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "WARNING:tensorflow:From D:\\AI-ML\\software\\Lib\\site-packages\\tf_keras\\src\\losses.py:2976: The name tf.losses.sparse_softmax_cross_entropy is deprecated. Please use tf.compat.v1.losses.sparse_softmax_cross_entropy instead.\n",
      "\n",
      "Starting Real-Time Emotion Detection... Press 'q' to quit.\n",
      "25-10-10 18:18:36 - 🔗 facial_expression_model_weights.h5 will be downloaded from https://github.com/serengil/deepface_models/releases/download/v1.0/facial_expression_model_weights.h5 to C:\\Users\\Arka Patra\\.deepface\\weights\\facial_expression_model_weights.h5...\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Downloading...\n",
      "From: https://github.com/serengil/deepface_models/releases/download/v1.0/facial_expression_model_weights.h5\n",
      "To: C:\\Users\\Arka Patra\\.deepface\\weights\\facial_expression_model_weights.h5\n",
      "100%|█████████████████████████████████████████████████████████████████████████████| 5.98M/5.98M [00:00<00:00, 8.19MB/s]\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Emotion detection stopped.\n"
     ]
    }
   ],
   "source": [
    "import cv2\n",
    "from deepface import DeepFace\n",
    "import pandas as pd\n",
    "from datetime import datetime\n",
    "import os\n",
    "\n",
    "# Initialize webcam\n",
    "cap = cv2.VideoCapture(0)\n",
    "\n",
    "# Create CSV file if not exists\n",
    "csv_file = \"emotions.csv\"\n",
    "if not os.path.exists(csv_file):\n",
    "    df = pd.DataFrame(columns=[\"Time\", \"Dominant Emotion\", \"All Emotions\"])\n",
    "    df.to_csv(csv_file, index=False)\n",
    "\n",
    "print(\"Starting Real-Time Emotion Detection... Press 'q' to quit.\")\n",
    "\n",
    "while True:\n",
    "    ret, frame = cap.read()\n",
    "    if not ret:\n",
    "        break\n",
    "\n",
    "    try:\n",
    "        # Analyze emotion using DeepFace\n",
    "        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)\n",
    "        dominant_emotion = result[0]['dominant_emotion']\n",
    "        emotion_scores = result[0]['emotion']\n",
    "\n",
    "        # Display emotion on screen\n",
    "        cv2.putText(frame, f'Emotion: {dominant_emotion}', (50, 50),\n",
    "                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)\n",
    "\n",
    "        # Log emotion with timestamp\n",
    "        now = datetime.now().strftime(\"%H:%M:%S\")\n",
    "        df = pd.DataFrame([[now, dominant_emotion, emotion_scores]], \n",
    "                          columns=[\"Time\", \"Dominant Emotion\", \"All Emotions\"])\n",
    "        df.to_csv(csv_file, mode='a', header=False, index=False)\n",
    "\n",
    "    except Exception as e:\n",
    "        print(\"Detection skipped (no face visible):\", e)\n",
    "\n",
    "    cv2.imshow(\"Emotion Detector\", frame)\n",
    "\n",
    "    # Quit key\n",
    "    if cv2.waitKey(1) & 0xFF == ord('q'):\n",
    "        break\n",
    "\n",
    "cap.release()\n",
    "cv2.destroyAllWindows()\n",
    "print(\"Emotion detection stopped.\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "721ad987-d12e-4d20-a08f-2b38c6d50246",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
