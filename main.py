import flet as ft
import re

# 원자량 데이터
ATOMIC_WEIGHTS = {
    'H': 1.008, 'He': 4.0026, 'Li': 6.94, 'Be': 9.0122, 'B': 10.81, 'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
    'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.085, 'P': 30.974, 'S': 32.06, 'Cl': 35.45, 'Ar': 39.95, 'K': 39.098, 'Ca': 40.078,
    'Sc': 44.956, 'Ti': 47.867, 'V': 50.942, 'Cr': 51.996, 'Mn': 54.938, 'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.38,
    'Ga': 69.723, 'Ge': 72.630, 'As': 74.922, 'Se': 78.971, 'Br': 79.904, 'Kr': 83.798, 'Rb': 85.468, 'Sr': 87.62, 'Y': 88.906, 'Zr': 91.224,
    'Nb': 92.906, 'Mo': 95.95, 'Tc': 98.0, 'Ru': 101.07, 'Rh': 102.91, 'Pd': 106.42, 'Ag': 107.87, 'Cd': 112.41, 'In': 114.82, 'Sn': 118.71,
    'Sb': 121.76, 'Te': 127.60, 'I': 126.90, 'Xe': 131.29, 'Cs': 132.91, 'Ba': 137.33, 'La': 138.91, 'Ce': 140.12, 'Pr': 140.91, 'Nd': 144.24,
    'Pm': 145.0, 'Sm': 150.36, 'Eu': 151.96, 'Gd': 157.25, 'Tb': 158.93, 'Dy': 162.50, 'Ho': 164.93, 'Er': 167.26, 'Tm': 168.93, 'Yb': 173.05,
    'Lu': 174.97, 'Hf': 178.49, 'Ta': 180.95, 'W': 183.84, 'Re': 186.21, 'Os': 190.23, 'Ir': 192.22, 'Pt': 195.08, 'Au': 196.97, 'Hg': 200.59,
    'Tl': 204.38, 'Pb': 207.2, 'Bi': 208.98, 'Po': 209.0, 'At': 210.0, 'Rn': 222.0, 'Fr': 223.0, 'Ra': 226.0, 'Ac': 227.0, 'Th': 232.04,
    'Pa': 231.04, 'U': 238.03, 'Np': 237.0, 'Pu': 244.0, 'Am': 243.0, 'Cm': 247.0, 'Bk': 247.0, 'Cf': 251.0, 'Es': 252.0, 'Fm': 257.0,
    'Md': 258.0, 'No': 259.0, 'Lr': 266.0, 'Rf': 267.0, 'Db': 268.0, 'Sg': 269.0, 'Bh': 270.0, 'Hs': 269.0, 'Mt': 278.0, 'Ds': 281.0,
    'Rg': 282.0, 'Cn': 285.0, 'Nh': 286.0, 'Fl': 289.0, 'Mc': 290.0, 'Lv': 293.0, 'Ts': 294.0, 'Og': 294.0
}

def parse_formula(formula):
    if not formula: return {}
    matches = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    elements = {}
    for el, count in matches:
        count = int(count) if count else 1
        elements[el] = elements.get(el, 0) + count
    return elements

def calculate_mw(elements_dict):
    mw = 0.0
    for el, count in elements_dict.items():
        if el not in ATOMIC_WEIGHTS:
            raise ValueError(f"데이터에 없는 원소: {el}")
        mw += ATOMIC_WEIGHTS[el] * count
    return mw
    
def find_ratio(react_dict, prod_dict):
    common_elements = set(react_dict.keys()) & set(prod_dict.keys())
    if not common_elements: return 1.0, None
    target_element = next((el for el in common_elements if el not in ['H', 'O', 'C', 'N']), None)
    if not target_element:
        target_element = list(common_elements)[0] if common_elements else None
    
    if target_element:
        return react_dict[target_element] / prod_dict[target_element], target_element
    return 1.0, None

def main(page: ft.Page):
    page.title = "스마트 수율 계산기"
    page.window_width = 400  
    page.window_height = 800
    page.scroll = "adaptive"
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- UI 컴포넌트 ---
    react_formula_input = ft.TextField(label="출발 물질 화학식", value="Nd2O3")
    react_mass_input = ft.TextField(label="투입량 (g)", value="10.0", keyboard_type=ft.KeyboardType.NUMBER)
    prod_formula_input = ft.TextField(label="생성물 화학식", value="NdF3")
    prod_mass_input = ft.TextField(label="실제 생산량 (g)", value="11.9", keyboard_type=ft.KeyboardType.NUMBER)
    
    result_text = ft.Text(size=18, weight="bold")
    # 수정 1: ft.colors.BLUE_GREY 대신 "blue_grey" 사용
    info_text = ft.Text(size=14, color="blue_grey") 

    # --- 계산 로직 ---
    def calculate(e=None):
        try:
            r_form = react_formula_input.value
            r_mass = float(react_mass_input.value)
            p_form = prod_formula_input.value
            p_mass = float(prod_mass_input.value)

            r_dict = parse_formula(r_form)
            p_dict = parse_formula(p_form)

            r_mw = calculate_mw(r_dict)
            p_mw = calculate_mw(p_dict)
            
            if r_mw == 0 or p_mw == 0:
                raise ValueError("분자량 계산 오류")

            ratio, target = find_ratio(r_dict, p_dict)
            theo_yield = (r_mass / r_mw) * ratio * p_mw
            percent_yield = (p_mass / theo_yield) * 100

            info_text.value = f"📌 {target} 기준 반응비: {ratio:.2f} \n(출발물질 MW: {r_mw:.2f}, 생성물 MW: {p_mw:.2f})"
            result_text.value = f"🎯 이론적 생산량: {theo_yield:.4f} g\n📈 최종 수율: {percent_yield:.2f} %"
            
            # 수정 2: 색상 문자열로 직접 할당
            result_text.color = "blue" if percent_yield <= 100 else "red"
            
        except Exception:
            result_text.value = "⚠️ 유효한 화학식과 숫자를 입력하세요."
            result_text.color = "red"
            info_text.value = ""
        
        page.update()

    # 입력값이 바뀔 때마다 자동 계산
    for control in [react_formula_input, react_mass_input, prod_formula_input, prod_mass_input]:
        control.on_change = calculate

    # 초기 계산 실행
    calculate()

   # --- 화면 배치 ---
    page.add(
        ft.SafeArea(
            ft.Column([
                ft.Text("💡 수율 & 반응비 자동 분석", size=22, weight="bold", color="indigo"),
                ft.Divider(),
                react_formula_input, react_mass_input,
                prod_formula_input, prod_mass_input,
                ft.Divider(),
                info_text,
                result_text
            ])
        )
    )

# 수정 4: 최신 권장 실행 방식 반영
ft.run(main)
