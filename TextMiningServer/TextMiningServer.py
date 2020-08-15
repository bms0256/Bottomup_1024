from flask import Flask, request
from konlpy.tag import Okt
from collections import Counter
from waitress import serve
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


app = Flask(__name__)
dic2 = {}

@app.route("/")
def frequency(): # 내부 IP 또는 도메인(DDNS):내부 포트 또는 외부 포트/인자
    
    body = request.args.get('name',"")
    word = request.args.get('word',"")

    
    noun_count = 50 # 출력할 상위 명사 개수

    dic2, tags = get_tags(body, noun_count, word) # get_tags 함수 호출
    
    wordcloud = WordCloud(max_font_size=200,font_path='C:\\Windows\\Fonts'\
                      '\\gulim.ttc',stopwords=STOPWORDS,background_color=\
                      '#FFFFFF',width=1200,height=800)\
                      .generate_from_frequencies(dic2)

    
    plt.figure(figsize=(10,8)) #화면의 크기 설정(인치 단위이다.)

    plt.imshow(wordcloud) #imshow는 이미지를 출력하는 메소드이다. wordcloud에 저장
                          #되어 있는 워드클라우드 이미지 데이터를 사용한다.

    plt.tight_layout(pad=0) #화면의 레이아웃을 설정한다. pad=0은 화면의 모서리와
                            #글자 사이의 여백이 0임을 의미한다. 그 외 나머지 설정
                            #들은 기본값으로 했다.

    plt.axis('off') #화면에 x,y축을 사용하지 않음으로 설정.

    plt.savefig('static/wordcloud.png', bbox_inches='tight')

                                     
    return tags


def get_tags(text, ntags, word): # 추출한 텍스트에서 명사를 분리&추출한 후 빈도를
                                # 계산하는 함수, 첫 번째 인자 text는 분석에 사용
                                # 할 텍스트이고, ntags는 분리한 명사들 중 결과
                                # 를 출력할 명사의 개수이다.

    spliter = Okt() # Okt 기능을 하는 객체 생성
    nouns = spliter.nouns(text) # noun 메소드(기능)로 text에서 명사만 분리&추출
                                # 그리고 그걸 순환가능한 객체로 저장
                                
    count = Counter(nouns) #분리 및 추출한 명사 빈도 계산
    
    return_str = "" # 계산한 빈도수를 저장하기 위해 스트링 변수 선언

    dic = {}
    
    for n, c in count.most_common(ntags): #입력받은 인자 ntags(정수)만큼 count
                                          #에 저장되어 있는 명사를 빈도수 큰거
                                          #부터 반환함. n에는 명사, c에는 빈도수가 저장됨.
        
        if len(n)!=1 and len(n)!=0:
            if word in n:
                continue
            elif n=="시간":
                continue
            elif "이후" in n:
                continue
            elif "지난" in n:
                continue
            elif "추가" in n:
                continue
            elif "관련" in n:
                continue
            elif "기자" in n:
                continue
            elif "사진" in n:
                continue
            elif "뉴스" in n:
                continue
            elif "오전" in n:
                continue
            elif "오후" in n:
                continue
            elif "인근" in n:
                continue
            elif "현재" in n:
                continue
            elif "최근" in n:
                continue
            elif "대한" in n:
                continue
            elif "위해" in n:
                continue
            elif "대해" in n:
                continue
            else:
                return_str += str(n) + " " + str(c) + " "
                if n=="진자":
                    dic["확진자"]=c
                else:
                    dic[n]=c
                
    return dic, return_str.replace("진자","확진자")#만든 문자열을 반환


if __name__ == "__main__": # 모든 호스트 대상 5000 포트를 개방하여 서버 구동
                           # frequency에서 인자로 받을 body 값의 request limit
                           # 을 10MB로 설정
    serve(app, host='0.0.0.0', port='5000',
          max_request_header_size=10000000)

