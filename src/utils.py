TJRO_BLUE = "#0c326f"

TJRO_IMAGE = "https://www.tjro.jus.br/templates/portal_tjro_helix_j5/images/presets/default/logo.png"

def footer():
    return f"""
    <div style="position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; text-align: center; color: #666; font-size: 12px; padding: 10px; border-top: 1px solid #eee; z-index: 1000;">
       Desenvolvido pelo <strong>Laboratório de Inovação Gênesis</strong> - TJRO <br>© 2025 CPCAD. Todos os direitos reservados. 
    </div>
    """

def render_svg_icon(svg_path):
    return f"""
    <div style="display: flex; justify-content: center; margin-bottom: 10px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="{TJRO_BLUE}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            {svg_path}
        </svg>
    </div>
    """