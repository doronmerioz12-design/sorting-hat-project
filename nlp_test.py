import wikipediaapi
from sentence_transformers import SentenceTransformer

# 1. הגדרת ויקיפדיה (חובה לציין User Agent כפי שלמדנו)
wiki = wikipediaapi.Wikipedia(
    user_agent="SortingHatProject/1.0 (contact: your_email@mail.huji.ac.il)",
    language='en'
)

# 2. טעינת המודל של Hugging Face (בפעם הראשונה זה יוריד את המודל הקטן למחשב)
print("טוען את מודל ה-AI... חכה רגע...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 3. שליפת טקסט על הארי פוטר
page = wiki.page("Harry Potter")
if page.exists():
    text = page.summary[:500]  # לוקחים רק את ההתחלה לבדיקה
    print(f"הטקסט שנמצא: {page.title}")

    # 4. יצירת הווקטור (הפיכת הטקסט למספרים)
    vector = model.encode(text)

    print("\nהצלחה! ווקטור התכונות נוצר.")
    print(f"אורך הווקטור: {len(vector)} מספרים.")
    print(f"חמשת המספרים הראשונים בווקטור: {vector[:5]}")
else:
    print("שגיאה: לא נמצא דף בויקיפדיה.")