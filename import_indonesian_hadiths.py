import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/mizan_db")

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dataset Sampel Hadis Terjemahan Bahasa Indonesia (Bukhari & Muslim)
DATASET_HADIS = [
    {
        "number": "1",
        "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ وَإِنَّمَا لِكُلِّ امْرِئٍ مَا نَوَى",
        "translation_id": "Sesungguhnya setiap amalan tergantung pada niatnya, dan setiap orang akan mendapatkan sesuai dengan apa yang ia niatkan. Barangsiapa yang hijrahnya karena Allah dan Rasul-Nya, maka hijrahnya kepada Allah dan Rasul-Nya."
    },
    {
        "number": "2",
        "arabic": "بُنِيَ الإِسْلَامُ عَلَى خَمْسٍ: شَهَادَةِ أَنْ لَا إِ لَهَ إِلَّا اللهُ وَأَنَّ مُحَمَّدًا رَسُولُ اللهِ، وَإِقَامِ الصَّلَاةِ، وَإِيتَاءِ الزَّكَاةِ، وَالحَجِّ، وَصَوْمِ رَمَضَانَ",
        "translation_id": "Islam dibangun di atas lima perkara: bersaksi bahwa tidak ada tuhan yang berhak disembah selain Allah dan Muhammad adalah utusan Allah, mendirikan shalat, menunaikan zakat, menunaikan ibadah haji, dan berpuasa di bulan Ramadhan."
    },
    {
        "number": "3",
        "arabic": "الْمُسْلِمُ مَنْ سَلِمَ الْمُسْلِمُونَ مِنْ لِسَانِهِ وَيَدِهِ",
        "translation_id": "Seorang muslim yang sejati adalah orang yang orang-orang muslim lainnya selamat dari gangguan lisan dan tangannya."
    },
    {
        "number": "4",
        "arabic": "مَنْ كَانَ يُؤْمِنُ بِاللَّهِ وَالْيَوْمِ الآخِرِ فَلْيَقُلْ خَيْرًا أَوْ لِيَصْمُتْ",
        "translation_id": "Barangsiapa yang beriman kepada Allah dan hari akhir, hendaklah ia berkata baik atau diam."
    },
    {
        "number": "5",
        "arabic": "لاَ يُؤْمِنُ أَحَدُكُمْ حَتَّى يُحِبَّ لأَخِيهِ مَا يُحِبُّ لِنَفْسِهِ",
        "translation_id": "Tidak sempurna iman salah seorang di antara kalian hingga ia mencintai saudaranya sebagaimana ia mencintai dirinya sendiri."
    },
    {
        "number": "6",
        "arabic": "طَلَبُ الْعِلْمِ فَرِيضَةٌ عَلَى كُلِّ مُسْلِمٍ",
        "translation_id": "Menuntut ilmu itu wajib atas setiap muslim."
    },
    {
        "number": "7",
        "arabic": "الدِّينُ النَّصِيحَةُ",
        "translation_id": "Agama itu adalah nasihat."
    },
    {
        "number": "8",
        "arabic": "إِنَّ اللَّهَ طَيِّبٌ لاَ يَقْبَلُ إِلاَّ طَيِّبًا",
        "translation_id": "Sesungguhnya Allah Maha Baik dan tidak menerima kecuali yang baik."
    },
    {
        "number": "9",
        "arabic": "اتَّقِ اللَّهِ حَيْثُمَا كُنْتَ وَأَتْبِعِ السَّيِّئَةَ الْحَسَنَةَ تَمْحُهَا وَخَالِقِ النَّاسَ بِخُلُقٍ حَسَنٍ",
        "translation_id": "Bertakwalah kepada Allah di mana saja engkau berada, iringilah keburukan dengan kebaikan niscaya kebaikan itu akan menghapusnya, dan pergatullah manusia dengan akhlak yang baik."
    },
    {
        "number": "10",
        "arabic": "الصَّلاَةُ نُورٌ وَالصَّدَقَةُ بُرْهَانٌ وَالصَّبْرُ ضِيَاءٌ",
        "translation_id": "Shalat adalah cahaya, sedekah adalah bukti, dan sabar adalah sinar."
    }
]

async def init_db_and_import():
    print("🚀 Memproses data hadis Bahasa Indonesia lokal...")

    async with AsyncSessionLocal() as session:
        print("📥 Memasukkan data ke PostgreSQL...")
        
        insert_query = text("""
            INSERT INTO hadiths (hadith_number, arabic, translation_id)
            VALUES (:hadith_number, :arabic, :translation_id)
            ON CONFLICT (hadith_number) 
            DO UPDATE SET 
                arabic = EXCLUDED.arabic,
                translation_id = EXCLUDED.translation_id;
        """)

        count = 0
        for item in DATASET_HADIS:
            await session.execute(
                insert_query,
                {
                    "hadith_number": str(item["number"]),
                    "arabic": item["arabic"],
                    "translation_id": item["translation_id"]
                }
            )
            count += 1

        await session.commit()
        print(f"🎉 SUKSES! Total {count} hadis Bahasa Indonesia berhasil masuk ke database!")

if __name__ == "__main__":
    asyncio.run(init_db_and_import())