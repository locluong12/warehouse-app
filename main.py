import streamlit as st
import streamlit.components.v1 as components

# --- Cấu hình trang ---
st.set_page_config(page_title="Warehouse Management", page_icon="📦", layout="wide")

# --- Biến cấu hình ---
ADMIN_PIN = "111222"

# --- Style tuỳ biến ---
st.markdown("""
<style>
    body { background-color: #f4f4f9; color: #333; font-size: 16px; }
    section[data-testid="stSidebar"] { background-color: #003366; color: white !important; }
    section[data-testid="stSidebar"] * { color: white !important; }
    .stSidebar .stTextInput input { color: black !important; background-color: white !important; }
    .stSidebar .stTextInput input::placeholder { color: white !important; }
    .sidebar-title { font-size: 18px; font-weight: bold; color: white !important; }
    div[data-baseweb="select"] > div { background-color: #2c3e90 !important; color: white !important; }
    div[data-baseweb="select"] > div:hover { background-color: #355caa !important; }
    .stButton > button { background-color: #0059b3; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .stButton > button:hover { background-color: #004080; }
    .stButton.active > button { background-color: #001f4d !important; }
    h1 { font-size: 28px; text-align: center; color: black; padding-top: 50px; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# Ẩn sidebar mặc định của Streamlit multi-page
st.markdown("""<style>[data-testid="stSidebarNav"] { display: none; }</style>""", unsafe_allow_html=True)

# --- Khởi tạo session state ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False
if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = "Quản lý kho"
if "selected_sub_menu" not in st.session_state:
    st.session_state.selected_sub_menu = "View Stock"

# --- Trang đăng nhập ---
if not st.session_state.authenticated:
    from login import login_page
    login_page()
    st.stop()

# --- MENU chính ---
menu = st.sidebar.selectbox(
    "",
    ["Quản lý kho", "Quản lý hệ thống"],
    index=["Quản lý kho", "Quản lý hệ thống"].index(st.session_state.selected_menu)
)

if menu != st.session_state.selected_menu:
    st.session_state.selected_menu = menu
    st.session_state.selected_sub_menu = (
        "View Stock" if menu == "Quản lý kho" else "Quản lý nhân viên"
    )
    st.rerun()

# --- SUB MENU: Quản lý kho ---
if menu == "Quản lý kho":
    sub_menus = ["View Stock", "Import Stock", "Export Stock", "Dashboard"]
    for sub in sub_menus:
        if st.sidebar.button(sub, key=sub, type="primary" if st.session_state.selected_sub_menu == sub else "secondary"):
            st.session_state.selected_sub_menu = sub
            st.rerun()

    if st.session_state.selected_sub_menu == "View Stock":
        from pages.view_stock import show_view_stock
        show_view_stock()
    elif st.session_state.selected_sub_menu == "Import Stock":
        from pages.import_stock import show_material_page
        show_material_page()
    elif st.session_state.selected_sub_menu == "Export Stock":
        from pages.export_stock import show_export_stock
        show_export_stock()
    elif st.session_state.selected_sub_menu == "Dashboard":
        from pages.dashboard import show_dashboard
        show_dashboard()

# --- SUB MENU: Quản lý hệ thống ---
elif menu == "Quản lý hệ thống":
    if not st.session_state.admin_authenticated:
        st.sidebar.markdown("### Nhập mã PIN để truy cập")
        input_pin = st.sidebar.text_input("Mã PIN", type="password")
        if st.sidebar.button("Xác nhận"):
            if input_pin == ADMIN_PIN:
                st.session_state.admin_authenticated = True
                st.success("✅ Truy cập thành công!")
                st.rerun()
            else:
                st.sidebar.error("❌ Sai mã PIN.")
        st.stop()

    sub_menus = ["Quản lý nhân viên", "Quản lý linh kiện", "Quản lý máy"]
    for sub in sub_menus:
        if st.sidebar.button(sub, key=sub, type="primary" if st.session_state.selected_sub_menu == sub else "secondary"):
            st.session_state.selected_sub_menu = sub
            st.rerun()

    if st.session_state.selected_sub_menu == "Quản lý nhân viên":
        from pages.employees import show_employees
        show_employees()
    elif st.session_state.selected_sub_menu == "Quản lý linh kiện":
        from pages.spare_parts import manage_spare_parts
        manage_spare_parts()
    elif st.session_state.selected_sub_menu == "Quản lý máy":
        from pages.machine import show_machine_page
        show_machine_page()

    # --- Nút thoát quyền quản lý ---
    st.sidebar.markdown("---")
    if st.sidebar.button("Thoát quyền quản lý"):
        st.session_state.admin_authenticated = False
        st.session_state.selected_menu = "Quản lý kho"
        st.session_state.selected_sub_menu = "View Stock"
        
        st.rerun()
