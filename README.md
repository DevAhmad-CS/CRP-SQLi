# SQL Injection Detection System

A machine learning-based web application for real-time SQL injection detection using Support Vector Machine (SVM) classification.

## 🚀 Features

- **Real-time Detection**: Analyze SQL queries instantly
- **High Accuracy**: 99.53% accuracy on test set
- **Low False Positive Rate**: 0.23%
- **Confidence Score**: Get detailed prediction probabilities
- **Modern UI**: Beautiful, responsive design with smooth animations
- **Fast Response**: Optimized for quick predictions

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **Python 3.8+**: Core programming language
- **Scikit-learn**: Machine learning library
- **SVM (Support Vector Machine)**: Classification algorithm
- **TF-IDF Vectorization**: Natural Language Processing

### Frontend
- **HTML5, CSS3, JavaScript**: Core web technologies
- **Vanta.js**: Animated background effects
- **Custom Animations**: Professional scroll and interaction animations

## 📊 Model Performance

- **Accuracy**: 99.53%
- **Precision**: 99.77%
- **Recall**: 99.19%
- **F1-Score**: 99.48%

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DevAhmad-CS/CRP-SQLi.git
   cd CRP-SQLi
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare models**
   - Place trained models in `models/` directory:
     - `svm_model.pkl`
     - `tfidf_vectorizer.pkl`

5. **Run the application**
   ```bash
   cd web_app
   python main.py
   ```

6. **Access the application**
   - Open browser: `http://localhost:8000`

## 📁 Project Structure

```
CRP-SQLi/
├── web_app/
│   ├── main.py              # FastAPI application
│   ├── static/
│   │   ├── css/             # Stylesheets
│   │   ├── js/              # JavaScript files
│   │   └── images/          # Images
│   └── templates/           # HTML templates
├── models/                  # ML models (not included)
├── .gitignore
└── README.md
```

## 🎯 Usage

1. Enter a SQL query in the input field
2. Click "Analyze Query"
3. View the prediction result with confidence score
4. Check detailed probabilities for normal/malicious classification

## 👨‍💻 Developer

**Ahmad Mahmoud**
- Computer Science Student at [Al-Hussein Technical University (HTU)](https://www.htu.edu.jo/)
- Web & Mobile Developer
- Machine Learning Research (SQLi Detection)

### Contact
- **Email**: ahmadmahmouddev@gmail.com
- **GitHub**: [DevAhmad-CS](https://github.com/DevAhmad-CS)
- **LinkedIn**: [ahmad-mahmoud-245883269](https://linkedin.com/in/ahmad-mahmoud-245883269)

## 📝 License

This project is for educational and research purposes.

## 🙏 Acknowledgments

- Al-Hussein Technical University (HTU)
- Scikit-learn community
- FastAPI framework

---

**Note**: This project was developed as part of academic research in SQL injection detection using machine learning techniques.
