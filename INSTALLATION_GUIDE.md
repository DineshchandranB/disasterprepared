# 🔧 INSTALLATION & SETUP INSTRUCTIONS

## Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- Code editor (VS Code recommended)

---

## Step-by-Step Installation

### 1. Navigate to Frontend Directory
```bash
cd "c:\Users\Hp\OneDrive\Desktop\Capstone project\disaster-prepareness"
```

### 2. Install Framer Motion (Required for Animations)
```bash
npm install framer-motion
```

### 3. Verify All Dependencies
```bash
npm install
```

This will install:
- react (19.2.4)
- react-dom (19.2.4)
- react-router-dom (7.13.0)
- framer-motion (latest)
- react-scripts (5.0.1)

### 4. Start Development Server
```bash
npm start
```

The app will open at: `http://localhost:3000`

---

## 🔍 Verify Installation

### Check if all pages load:
1. Go to `http://localhost:3000`
2. Sign up with test data
3. Login
4. From Dashboard, click each sidebar item:
   - ✅ Emergency Contacts
   - ✅ Evacuation Routes
   - ✅ Disaster Checklist
   - ✅ Alerts Center
   - ✅ Report Incident
   - ✅ Risk Profile
   - ✅ Volunteer

### Expected Result:
- No console errors
- Smooth page transitions
- Animations working
- Forms functional
- Data persisting in localStorage

---

## 🐛 Troubleshooting

### Error: "Cannot find module 'framer-motion'"
**Solution:**
```bash
npm install framer-motion --save
```

### Error: "React Router not found"
**Solution:**
```bash
npm install react-router-dom --save
```

### Error: Port 3000 already in use
**Solution:**
```bash
# Kill the process on port 3000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use a different port:
PORT=3001 npm start
```

### Error: Module not found in pages
**Solution:**
Check that all files exist in `src/pages/`:
```bash
dir src\pages
```

Should show:
- EmergencyContacts.js & .css
- EvacuationRoutes.js & .css
- DisasterChecklist.js & .css
- AlertsCenter.js & .css
- IncidentReporting.js & .css
- RiskProfile.js & .css
- VolunteerCoordination.js & .css

---

## 📦 Package.json Check

Your `package.json` should include:

```json
{
  "dependencies": {
    "react": "^19.2.4",
    "react-dom": "^19.2.4",
    "react-router-dom": "^7.13.0",
    "framer-motion": "^11.0.0",
    "react-scripts": "5.0.1"
  }
}
```

If missing, run:
```bash
npm install react react-dom react-router-dom framer-motion react-scripts
```

---

## 🚀 Production Build

### Create optimized build:
```bash
npm run build
```

This creates a `build/` folder with:
- Minified JavaScript
- Optimized CSS
- Compressed assets
- Ready for deployment

### Test production build locally:
```bash
npm install -g serve
serve -s build
```

---

## 🌐 Deployment Options

### Option 1: Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Option 2: Netlify
```bash
npm install -g netlify-cli
netlify deploy
```

### Option 3: GitHub Pages
```bash
npm install gh-pages --save-dev
```

Add to `package.json`:
```json
{
  "homepage": "https://yourusername.github.io/disaster-preparedness",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}
```

Then deploy:
```bash
npm run deploy
```

---

## 🔧 Backend Setup (Optional)

### Start Flask Backend:
```bash
cd "c:\Users\Hp\OneDrive\Desktop\Capstone project\ai-backend"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend will run on: `http://localhost:5000`

### Update API URLs in Frontend:
Edit `src/utils/api.js`:
```javascript
const API_BASE_URL = "http://localhost:5000";
```

---

## 📱 Mobile Testing

### Test on mobile device:
1. Find your local IP:
```bash
ipconfig
```

2. Access from mobile:
```
http://YOUR_IP:3000
```

Example: `http://192.168.1.100:3000`

---

## 🧪 Testing Checklist

### Functional Tests:
- [ ] All pages load without errors
- [ ] Navigation works from Dashboard
- [ ] Forms can be submitted
- [ ] Data persists after refresh
- [ ] Animations are smooth
- [ ] Buttons are clickable
- [ ] LocalStorage is working

### Browser Compatibility:
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

### Responsive Design:
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

---

## 📊 Performance Optimization

### Check bundle size:
```bash
npm run build
```

Look for:
- `build/static/js/main.[hash].js` < 500KB
- `build/static/css/main.[hash].css` < 100KB

### Optimize if needed:
```bash
npm install --save-dev webpack-bundle-analyzer
```

---

## 🔐 Environment Variables

### Create `.env` file in root:
```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_WEATHER_API_KEY=your_key_here
REACT_APP_MAPS_API_KEY=your_key_here
```

### Access in code:
```javascript
const API_URL = process.env.REACT_APP_API_URL;
```

---

## 📝 Development Tips

### Hot Reload:
Changes auto-refresh in browser

### Console Logging:
Use React DevTools extension

### Debugging:
```javascript
console.log('Debug:', data);
```

### Code Formatting:
```bash
npm install --save-dev prettier
npx prettier --write "src/**/*.{js,jsx,css}"
```

---

## ✅ Success Indicators

You'll know everything is working when:
1. ✅ No errors in browser console
2. ✅ All pages load instantly
3. ✅ Animations are smooth (60fps)
4. ✅ Forms submit successfully
5. ✅ Data persists after refresh
6. ✅ Mobile responsive works
7. ✅ Navigation is seamless

---

## 🎉 You're Ready!

Your disaster preparedness platform is now:
- ✅ Fully installed
- ✅ All dependencies resolved
- ✅ Running smoothly
- ✅ Ready for development
- ✅ Ready for deployment

**Start building amazing features! 🚀**

---

## 📞 Support

If you encounter issues:
1. Check console for errors
2. Verify all files are present
3. Clear browser cache
4. Delete `node_modules` and reinstall:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

---

**Happy Coding! 💻**
