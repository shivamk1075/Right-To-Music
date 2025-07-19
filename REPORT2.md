# Audio-Match Grid Search Report

This report presents the results of a grid search performed to optimize parameters for the Audio-Match fingerprinting and song identification system. The goal was to maximize Top-5 accuracy for song snippet recognition.

## Best Result
**Best Top-5 Accuracy:** 53.33%  
**Best Parameter Set:**
```
{'coef1': 0.25, 'coef2': 0.5, 'targetZoneSize1': 8, 'targetZoneSize2': 2, 'threshold': 7, 'tolerance': 100}
```

---

## Full Grid Search Log
Below is the complete log of the grid search run, showing predictions and ranks for each test snippet:
============================================================
Grid Search Report
============================================================


=== Testing with parameters: {'coef1': 0.25, 'coef2': 0.5, 'targetZoneSize1': 8, 'targetZoneSize2': 2, 'threshold': 7, 'tolerance': 100} ===
Testing: song10_snippet1.mp3
Top-3 predictions: ['Banjaara', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'M Bole To', 'DJ Waley Babu - PagalSongs.com', 'Suit Suit']
Correct label 'Dua (Article 370)_320-(Fun2Desi.Com)' found at rank 2
Top-1 prediction: Banjaara
----------------------------------------
Testing: song10_snippet2.mp3
Top-3 predictions: ['Hawa Hawai', 'Banjaara', 'Suit Suit', 'DJ Waley Babu - PagalSongs.com', 'Hanuman Chalisa(PagalWorld.com.se)']
Correct label 'Dua (Article 370)_320-(Fun2Desi.Com)' not in top-5
Top-1 prediction: Hawa Hawai
----------------------------------------
Testing: song10_snippet4.mp3
Top-3 predictions: ['M Bole To', 'Suit Suit', 'DJ Waley Babu - PagalSongs.com', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'Falak Tak']
Correct label 'Dua (Article 370)_320-(Fun2Desi.Com)' found at rank 4
Top-1 prediction: M Bole To
----------------------------------------
Testing: song1_snippet1.mp3
Top-3 predictions: ['DJ Waley Babu - PagalSongs.com', 'Banjaara', 'Falak Tak']
Correct label 'Banjaara' found at rank 2
Top-1 prediction: DJ Waley Babu - PagalSongs.com
----------------------------------------
Testing: song1_snippet2.mp3
Top-3 predictions: ['Banjaara', 'Suit Suit', 'Hawa Hawai', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'DJ Waley Babu - PagalSongs.com']
Correct label 'Banjaara' found at rank 1
Top-1 prediction: Banjaara
----------------------------------------
Testing: song1_snippet4.mp3
Top-3 predictions: ['Suit Suit', 'Hawa Hawai', 'DJ Waley Babu - PagalSongs.com', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'Banjaara']
Correct label 'Banjaara' found at rank 5
Top-1 prediction: Suit Suit
----------------------------------------
Testing: song2_snippet1.mp3
Top-3 predictions: ['M Bole To', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'Hawa Hawai', 'DJ Waley Babu - PagalSongs.com', 'Hanuman Chalisa(PagalWorld.com.se)']
Correct label 'M Bole To' found at rank 1
Top-1 prediction: M Bole To
----------------------------------------
Testing: song2_snippet2.mp3
Top-3 predictions: ['Suit Suit', 'Hawa Hawai', 'Banjaara', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'Hanuman Chalisa(PagalWorld.com.se)']
Correct label 'M Bole To' not in top-5
Top-1 prediction: Suit Suit
----------------------------------------
Testing: song2_snippet4.mp3
Top-3 predictions: ['Hawa Hawai', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'Suit Suit', 'M Bole To', 'Banjaara']
Correct label 'M Bole To' found at rank 4
Top-1 prediction: Hawa Hawai
----------------------------------------
Testing: song3_snippet1.mp3
Top-3 predictions: ['Suit Suit', 'M Bole To', 'Hanuman Chalisa(PagalWorld.com.se)', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'DJ Waley Babu - PagalSongs.com']
Correct label 'Hanuman Chalisa(PagalWorld.com.se)' found at rank 3
Top-1 prediction: Suit Suit
----------------------------------------
Testing: song3_snippet2.mp3
Top-3 predictions: ['Banjaara', 'Hanuman Chalisa(PagalWorld.com.se)', 'Hawa Hawai', 'Suit Suit', 'Dua (Article 370)_320-(Fun2Desi.Com)']
Correct label 'Hanuman Chalisa(PagalWorld.com.se)' found at rank 2
Top-1 prediction: Banjaara
----------------------------------------
Testing: song3_snippet4.mp3
Top-3 predictions: ['Suit Suit', 'Banjaara', 'Hanuman Chalisa(PagalWorld.com.se)', 'Hawa Hawai', 'Dua (Article 370)_320-(Fun2Desi.Com)']
Correct label 'Hanuman Chalisa(PagalWorld.com.se)' found at rank 3
Top-1 prediction: Suit Suit
----------------------------------------
Testing: song4_snippet1.mp3
Top-3 predictions: ['Hawa Hawai', 'Suit Suit', 'Banjaara', 'M Bole To', 'Dua (Article 370)_320-(Fun2Desi.Com)']
Correct label 'Suit Suit' found at rank 2
Top-1 prediction: Hawa Hawai
----------------------------------------
Testing: song4_snippet2.mp3
Top-3 predictions: ['Suit Suit', 'M Bole To', 'Hawa Hawai', 'Hanuman Chalisa(PagalWorld.com.se)', 'Dua (Article 370)_320-(Fun2Desi.Com)']
Correct label 'Suit Suit' found at rank 1
Top-1 prediction: Suit Suit
----------------------------------------
Testing: song4_snippet4.mp3
Top-3 predictions: ['Suit Suit', 'Hawa Hawai', 'DJ Waley Babu - PagalSongs.com', 'M Bole To', 'Dua (Article 370)_320-(Fun2Desi.Com)']
Correct label 'Suit Suit' found at rank 1
Top-1 prediction: Suit Suit
----------------------------------------
Testing: song5_snippet1.mp3
Top-3 predictions: ['Suit Suit', 'Banjaara', 'Hanuman Chalisa(PagalWorld.com.se)', 'Hawa Hawai', 'Dua (Article 370)_320-(Fun2Desi.Com)']
Correct label 'I Love You(PagalWorldl)' not in top-5
Top-1 prediction: Suit Suit
----------------------------------------
Testing: song5_snippet2.mp3
Top-3 predictions: ['Suit Suit', 'Hawa Hawai', 'Banjaara', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'Hanuman Chalisa(PagalWorld.com.se)']
Correct label 'I Love You(PagalWorldl)' not in top-5
Top-1 prediction: Suit Suit
----------------------------------------
Testing: song5_snippet4.mp3
Top-3 predictions: ['Suit Suit', 'DJ Waley Babu - PagalSongs.com', 'Hawa Hawai', 'Falak Tak', 'M Bole To']
Correct label 'I Love You(PagalWorldl)' not in top-5
Top-1 prediction: Suit Suit
----------------------------------------
Testing: song6_snippet1.mp3
Top-3 predictions: ['Hawa Hawai', 'Suit Suit', 'Hanuman Chalisa(PagalWorld.com.se)', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'M Bole To']
Correct label 'Hawa Hawai' found at rank 1
Top-1 prediction: Hawa Hawai
----------------------------------------
Testing: song6_snippet2.mp3
Top-3 predictions: ['Hawa Hawai', 'Suit Suit', 'DJ Waley Babu - PagalSongs.com', 'M Bole To', 'Dua (Article 370)_320-(Fun2Desi.Com)']
Correct label 'Hawa Hawai' found at rank 1
Top-1 prediction: Hawa Hawai
----------------------------------------
Testing: song6_snippet4.mp3
Top-3 predictions: ['Suit Suit', 'Hawa Hawai', 'M Bole To', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'Hanuman Chalisa(PagalWorld.com.se)']
Correct label 'Hawa Hawai' found at rank 2
Top-1 prediction: Suit Suit
----------------------------------------
Testing: song7_snippet1.mp3
Top-3 predictions: ['Banjaara', 'Suit Suit', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'Hawa Hawai', 'Hanuman Chalisa(PagalWorld.com.se)']
Correct label 'Falak Tak' not in top-5
Top-1 prediction: Banjaara
----------------------------------------
Testing: song7_snippet2.mp3
Top-3 predictions: ['Banjaara', 'Suit Suit', 'Hawa Hawai', 'Hanuman Chalisa(PagalWorld.com.se)', 'Dua (Article 370)_320-(Fun2Desi.Com)']
Correct label 'Falak Tak' not in top-5
Top-1 prediction: Banjaara
----------------------------------------
Testing: song7_snippet4.mp3
Top-3 predictions: ['M Bole To', 'Suit Suit', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'Hawa Hawai', 'DJ Waley Babu - PagalSongs.com']
Correct label 'Falak Tak' not in top-5
Top-1 prediction: M Bole To
----------------------------------------
Testing: song8_snippet1.mp3
Top-3 predictions: ['Suit Suit', 'Banjaara', 'Hawa Hawai', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'DJ Waley Babu - PagalSongs.com']
Correct label 'Bekhayali - PagalNew' not in top-5
Top-1 prediction: Suit Suit
----------------------------------------
Testing: song8_snippet2.mp3
Top-3 predictions: ['Suit Suit', 'Hawa Hawai', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'Banjaara', 'Hanuman Chalisa(PagalWorld.com.se)']
Correct label 'Bekhayali - PagalNew' not in top-5
Top-1 prediction: Suit Suit
----------------------------------------
Testing: song8_snippet4.mp3
Top-3 predictions: ['Banjaara', 'Suit Suit', 'Hawa Hawai', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'Hanuman Chalisa(PagalWorld.com.se)']
Correct label 'Bekhayali - PagalNew' not in top-5
Top-1 prediction: Banjaara
----------------------------------------
Testing: song9_snippet1.mp3
Top-3 predictions: ['Hawa Hawai', 'Suit Suit', 'Banjaara', 'Hanuman Chalisa(PagalWorld.com.se)', 'Dua (Article 370)_320-(Fun2Desi.Com)']
Correct label 'DJ Waley Babu - PagalSongs.com' not in top-5
Top-1 prediction: Hawa Hawai
----------------------------------------
Testing: song9_snippet2.mp3
Top-3 predictions: ['Hawa Hawai', 'Suit Suit', 'Banjaara', 'Dua (Article 370)_320-(Fun2Desi.Com)', 'Hanuman Chalisa(PagalWorld.com.se)']
Correct label 'DJ Waley Babu - PagalSongs.com' not in top-5
Top-1 prediction: Hawa Hawai
----------------------------------------
Testing: song9_snippet4.mp3
Top-3 predictions: ['Dua (Article 370)_320-(Fun2Desi.Com)', 'M Bole To', 'Hawa Hawai', 'Suit Suit', 'Hanuman Chalisa(PagalWorld.com.se)']
Correct label 'DJ Waley Babu - PagalSongs.com' not in top-5
Top-1 prediction: Dua (Article 370)_320-(Fun2Desi.Com)
----------------------------------------

Top-5 accuracy: 53.33%

New best accuracy!



=== Final Best Parameter Set(s) ===
{'coef1': 0.25, 'coef2': 0.5, 'targetZoneSize1': 8, 'targetZoneSize2': 2, 'threshold': 7, 'tolerance': 100}
Best Top-5 Accuracy: 53.33%
