# 🚀 Deployment Guide - Step by Step

## 📋 **Pre-Deployment Checklist**

✅ Dashboard working locally: http://localhost:8501  
✅ No sample data dependencies (production ready)  
✅ Real API integration (NewsAPI + RSS fallback)  
✅ Clean project structure  
✅ All dependencies listed in requirements.txt  

## 🔧 **Step 1: GitHub Repository Setup**

### Option A: Command Line (Recommended)
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Make initial commit
git commit -m "Deploy: News Sentiment Analysis Dashboard"

# Create repository on GitHub.com first, then:
git remote add origin https://github.com/YOUR_USERNAME/news-sentiment-analysis.git
git branch -M main
git push -u origin main
```

### Option B: GitHub Desktop
1. Open GitHub Desktop
2. Create new repository from existing folder
3. Choose this project folder
4. Publish to GitHub

## 🌐 **Step 2: Streamlit Cloud Deployment**

### 1. Visit Streamlit Cloud
- Go to: https://share.streamlit.io/
- Sign in with GitHub account

### 2. Create New App
- Click "New app"
- Connect your GitHub repository
- Settings:
  - **Repository**: `your-username/news-sentiment-analysis`
  - **Branch**: `main` 
  - **Main file path**: `dashboard.py`
  - **Python version**: `3.11`

### 3. Add API Key (Important!)
- In app settings, go to "Secrets"
- Add this content:
```toml
NEWS_API_KEY = "your_actual_newsapi_key_here"
```

## 🔑 **Step 3: Get NewsAPI Key (Free)**

1. Visit: https://newsapi.org/register
2. Sign up for free account
3. Copy your API key
4. Add to Streamlit Cloud secrets (Step 2.3 above)

## 🎯 **Step 4: Deploy!**

- Click "Deploy" in Streamlit Cloud
- Wait 2-3 minutes for deployment
- Your app will be live at: `https://your-app-name.streamlit.app`

## ✨ **Post-Deployment**

### Features Your Live App Will Have:
- 📰 **Real-time news** from NewsAPI + RSS feeds
- 🤖 **AI sentiment analysis** with PySpark ML
- 📊 **Interactive dashboard** with live charts  
- 🔄 **Auto-refresh** capabilities
- 📱 **Mobile responsive** design
- 🌐 **24/7 availability**

### Sharing Your App:
- Share the live URL with anyone
- No installation needed for users
- Works on all devices and browsers

## 🚨 **Troubleshooting**

### Common Issues:
1. **Build fails**: Check requirements.txt for version conflicts
2. **No data**: Verify NewsAPI key in secrets
3. **RSS fails**: Normal fallback behavior, app still works
4. **Slow initial load**: First-time setup runs automatically

### Need Help?
- Check Streamlit Cloud logs for detailed errors
- Verify all files are committed to GitHub
- Ensure secrets are properly formatted

---

## 🎉 **Ready to Deploy!**

Your project is production-ready. Follow the steps above to get it live in about 10 minutes!