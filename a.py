import streamlit as st
import matplotlib.pyplot as plt 

st.title("반도체 공정 시뮬레이터")

st.sidebar.header("공정 조건 선택")
process = st.sidebar.selectbox("공정 선택",["산화","식각","증착"])
temp = st.sidebar.slider("온도(°C)", 200, 1000, 600)
time = st.sidebar.slider("공정 시간(분)", 1, 120, 30)

st.write(f"선택한 공정: **{process}**, 온도: {temp}°C, 시간: {time}분")

import streamlit as st
import matplotlib.pyplot as plt

# 예시 변수 입력 (실제로는 st.slider 또는 st.number_input 등으로 받아야 함)
process = "산화"
time = st.number_input("Time (min)", min_value=0.0, value=60.0)
temp = st.number_input("Temperature (°C)", min_value=800, value=1000)

process = "산화"
time = st.number_input("Time (min)", min_value=0.0, value=60.0)
temp = st.number_input("Temperature (°C)", min_value=800.0, value=1000.0)

if process == "산화":
    # A, B 값 설정 (예: Dry O2 at 1000°C 기준)
    A = 0.1       # μm
    B = 0.0117    # μm²/min

    # 시간 배열 만들기 (0부터 time까지 100개 점)
    times = np.linspace(0, time, 100)

    # 각 시간에 대한 산화막 두께 계산
    thicknesses = [(-A + np.sqrt(A**2 + 4 * B * t_i)) / 2 * 1000 for t_i in times]  # nm

    # 마지막 시간의 두께 출력
    final_thickness = thicknesses[-1]
    st.write(f"예상 산화막 두께: **{round(final_thickness, 2)} nm**")

    # 곡선 그래프 그리기
    fig, ax = plt.subplots()
    ax.plot(times, thicknesses, label="Oxide Thickness")
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Oxide Thickness (nm)")
    ax.set_title("Change in Oxide Thickness (Deal-Grove Model)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
  
#증착 시뮬레이션
elif process == "증착":
 deposition_rate = 0.08* (temp/100) # 단위: nm/min
 deposited_thickness = deposition_rate * time
 st.write(f"예상 증착막 두께: **{round(deposited_thickness, 2)} nm**")
 
 fig, ax = plt.subplots()
 ax.plot([0, time], [0, deposited_thickness]) 
 ax.set_xlabel("Time (min)")
 ax.set_ylabel("Deposited Thickness (nm)") 
 ax.set_title("Change in Deposited Thickness")
 st.pyplot(fig)

#이론 설명
st.markdown("---")
with st.expander("공정 이론 보기"):
 if process=="산화":
  st.markdown("""
  -**산화 공정**은 실리콘 표면에 산화막(SiO2)을 형성하는 과정입니다.
  -고온에서 02 또는 H2O 를 반응시켜 이루어지며, **Dry** 또는 **Wet 산화** 방식이 있습니다.
  """)
 elif process =="식각":
  st.markdown("""
  -**식각 공정**은 불필요한 박막을 제거하는 과정입니다.
  -**습식식각(Wet Etching)**과 **건식 식각(Dry Etching)** 방식이 있으며, 정밀도가 중요합니다. 
  """)
 elif process == "증착":
  st.markdown("""
  -**증착 공정**은 표면에 원하는 물질을 얇게 쌓아 올리는 과정입니다.
  -대표적으로 **CVD (화학 기상 증착)**, **PVD (물리적 기상 증착)** 방식이 사용됩니다.
  """)
#공정 시뮬레이터 제목 및 입력 받기
#산화, 식각, 증착 공정 시각화
#결과 그래프와 이론 설명 포함
