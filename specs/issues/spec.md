# Specification: Resolving Deployment and Backend/RAG Issues

## 1. Frontend Deployment Issue: GitHub Pages CSS/JS Loading Failure

### Description
Jab book ko GitHub Pages par deploy kiya jata hai, toh HTML content theek se load ho jata hai lekin CSS (styling) aur JavaScript files load nahi ho pate. Is ki wajah se book ki UI/UX kharab ho jati hai aur interactive elements kaam nahi karte. Local development environment mein yeh masla maujood nahi hai, book bilkul sahi display hoti hai aur functioning bhi theek hoti hai. Yeh masla production deployment mein hi zahir ho raha hai.

### Requirements
- GitHub Pages par deploy ki gayi book ke liye CSS files sahi tareeqay se load hon.
- GitHub Pages par deploy ki gayi book ke liye JavaScript files sahi tareeqay se load hon.
- Book ki UI/UX local environment jaisi ho.
- Console mein koi CSS ya JavaScript loading errors na hon.

### Success Criteria
- Deployed book ka URL open karne par, book ka layout aur styling waisa hi dikhe jaisa local par hai.
- Deployed book ke interactive components (agar koi hain) sahi tarah se kaam karein.
- Browser ke developer tools console mein CSS ya JavaScript se mutaliq koi errors na hon.
- Docusaurus build process mein koi warnings ya errors na hon jo deployment ko mutasir kar rahe hon.

## 2. Backend, RAG System, aur Qdrant Data Ingestion Issue

### Description
Backend server sahi tareeqay se respond nahi kar raha. Jab chatbot se interaction ki jati hai, toh "Error contacting bot. Please try again." ka message milta hai. Is ke ilawa, Qdrant database mein book ke content ke bajaye dusra content bhi ingest ho gaya hai, jaisa ke "Context found: "Smart Chat..."..." se zahir hota hai. Humara maqsad sirf book ka content RAG system ke liye database mein dalna tha. Is ka matlab hai ke data ingestion process ya RAG setup mein ghalati hai.

### Requirements
- Backend server sahi tareeqay se chal raha ho aur chatbot requests ko process kar sake.
- Chatbot "Error contacting bot. Please try again." ka error na de.
- Qdrant database mein sirf book ka content hi ingest ho, koi bhi gair-mutalliq (irrelevant) content nahi.
- RAG system users ke selected text aur queries par book ke content se relevant jawab de.
- Backend aur Qdrant ke درمیان communication sahi tareeqay se ho.

### Success Criteria
- Chatbot ko 'hi' message bhejte hi, woh sahi tareeqay se respond kare, na ke error message de.
- Chatbot, book ke kisi bhi hisse se copy kiye gaye text par ya us se mutalliq sawalon par, sirf book ke content se related jawab de.
- Qdrant database mein maujood data ko verify kiya jaye ke usmein sirf book ka content hai aur koi bhi extraneous data nahi.
- Selected text functionality RAG system ke saath sahi kaam kare.
- Backend logs mein koi serious errors na hon jo RAG ya Qdrant interaction se mutalliq hon.

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
