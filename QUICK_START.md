# 🚀 QUICK START GUIDE - New Pages

## Installation & Setup

### 1. Install Dependencies (if not already done)
```bash
cd disaster-prepareness
npm install framer-motion
```

### 2. Verify All Files Are Present
```
src/pages/
├── EmergencyContacts.js ✅
├── EmergencyContacts.css ✅
├── EvacuationRoutes.js ✅
├── EvacuationRoutes.css ✅
├── DisasterChecklist.js ✅
├── DisasterChecklist.css ✅
├── AlertsCenter.js ✅
├── AlertsCenter.css ✅
├── IncidentReporting.js ✅
├── IncidentReporting.css ✅
├── RiskProfile.js ✅
├── RiskProfile.css ✅
├── VolunteerCoordination.js ✅
└── VolunteerCoordination.css ✅
```

### 3. Start the Application
```bash
npm start
```

### 4. Test Navigation
1. Go to `http://localhost:3000`
2. Sign up with any details
3. Login
4. From Dashboard sidebar, click on any new page:
   - 🚨 Emergency Contacts
   - 🗺️ Evacuation Routes
   - 📋 Disaster Checklist
   - 🔔 Alerts Center
   - 📢 Report Incident
   - 📊 Risk Profile
   - 🤝 Volunteer

---

## 🎯 Quick Feature Test

### Emergency Contacts
1. Click "Add Contact"
2. Fill in name, phone, relationship
3. Click "Save Contact"
4. Test "Call", "SMS", "Share Location" buttons
5. Click "SEND MASS ALERT" to test alert all

### Evacuation Routes
1. Enter a destination (e.g., "City Hospital")
2. Click "Calculate Routes"
3. View 3 route options with risk scores
4. Click on shelters to select as destination

### Disaster Checklist
1. Update household profile (adults, children, pets, elderly)
2. See smart recommendations appear
3. Select disaster type (Earthquake, Flood, etc.)
4. Check off items
5. Watch progress bar update
6. Add custom items

### Alerts Center
1. View active alerts
2. Check severity levels (Critical, Severe, Warning, Info)
3. See verified badges
4. Click "View Details" or "Share"

### Incident Reporting
1. Click "Report Incident"
2. Select type, enter location and description
3. Submit report
4. See it appear in the feed
5. Upvote incidents

### Risk Profile
1. View your risk score (0-10)
2. See breakdown of 5 risk factors
3. Read AI-generated recommendations
4. Check risk trend

### Volunteer Coordination
1. View available opportunities
2. Check urgency levels and required skills
3. Click "Sign Up" for a shift
4. See it appear in "My Upcoming Shifts"

---

## 🐛 Troubleshooting

### Issue: Pages not loading
**Solution:** Check that all imports in App.js are correct

### Issue: Animations not working
**Solution:** Ensure framer-motion is installed:
```bash
npm install framer-motion
```

### Issue: Navigation not working
**Solution:** Verify react-router-dom is installed:
```bash
npm install react-router-dom
```

### Issue: Styles not applying
**Solution:** Check that CSS files are imported in each component

---

## 📝 Notes

- All data is stored in **localStorage** (no backend required for testing)
- Mock data is used for demonstrations
- Pages are fully responsive (mobile-friendly)
- All pages include smooth animations
- Ready for backend API integration

---

## 🎨 Customization

### Change Colors
Edit the gradient backgrounds in each CSS file:
```css
background: linear-gradient(135deg, #color1 0%, #color2 100%);
```

### Add More Features
Each component is modular and easy to extend:
- Add new form fields
- Include more data points
- Integrate real APIs
- Add database connections

---

## ✅ Success Checklist

- [ ] All 7 new pages load without errors
- [ ] Navigation from Dashboard works
- [ ] Forms can be submitted
- [ ] Data persists in localStorage
- [ ] Animations are smooth
- [ ] Mobile responsive design works
- [ ] All buttons are clickable

---

## 🎉 You're All Set!

Your disaster preparedness platform now has **10 fully functional pages** with beautiful UI, smooth animations, and comprehensive features.

**Next Steps:**
1. Connect to backend APIs
2. Add real-time data
3. Implement user authentication
4. Deploy to production
5. Add more advanced features

**Happy Coding! 🚀**
