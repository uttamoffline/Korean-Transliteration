# Korean Romanizer
For Korean learners it can be really difficult to sound out Korean words properly (considering there are many exceptions to pronunciation that result from sound dropping or how slow/fast someone is talking). To provide a rough English approximation, this romanizer takes Korean strings and outputs English transliteration using different rules. These rules include consonant assimilation, double consonant finals, vowel followed by a consonant final, and a few others. The romanizer hyphenates the English transliteration so that every character in the Korean input can be compared to some transliterated English component (usually, hyphens are reserved to resolve confusion). 

# Usage
```
example_1 = Romanizer('안녕하세요 ㅋㅋ.').romanize()
print(example_1) -> an-nyeong-ha-se-yo k-k.

example_2 = Romanizer('종로, 그렇지, 입학, 행복하다, 곧할거야').romanize()
print(example_2) -> jong-no, geu-reo-chi, ip-pak, haeng-bok-ka-da, got-tal-geo-ya
```
# Useful Links
[National Institute of Korean Language (Romanization of Korean)](https://www.korean.go.kr/front_eng/roman/roman_01.do)

[Korean Jamo and Unicode](http://gernot-katzers-spice-pages.com/var/korean_hangul_unicode.html#:~:text=The%20Hangul%20syllabary%20occupies%20the,used%20for%20encoding%20Korean%20text)

[Canonical and Compatibility Equivalence (aka more Unicode)](http://unicode.org/reports/tr15/#Canon_Compat_Equivalence)
