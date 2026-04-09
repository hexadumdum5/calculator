import flet as ft
import re

# 원자량 데이터
ATOMIC_WEIGHTS = {
    'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998,
    'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.085, 'P': 30.974,
    'S': 32.06, 'Cl': 35.45, 'K': 39.098, 'Ca': 40.078, 'Nd': 144.24,
    # 필요시 다른 원소들도 자유롭게 추가하세요
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
    return sum(ATOMIC_WEIGHTS.get(el, 0) * count for el, count in elements_dict.items())

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
