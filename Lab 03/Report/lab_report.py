import os
import re
try:
    import docx
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls
except ImportError:
    print("The 'python-docx' library is missing. Please install it using: pip install python-docx")
    exit()

# --- Core Styling Helpers (Inherited from Reference) ---
COLOR_PRIMARY = RGBColor(0, 51, 102)     # Deep Navy
COLOR_SECONDARY = RGBColor(70, 130, 180) # Steel Blue
COLOR_TEXT = RGBColor(40, 40, 40)        # Charcoal
COLOR_MUTED = RGBColor(120, 120, 120)    # Gray
HEX_PRIMARY_BG = "EBF3FA"
HEX_CODE_BG = "F8F9FA"
HEX_BOX_BG = "FAFAFA"

def set_cell_background(cell, fill_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", color="CCCCCC", sz="4"):
    def border_tag(side, val):
        if val == "none":
            return f'<w:{side} {nsdecls("w")} w:val="none"/>'
        return f'<w:{side} {nsdecls("w")} w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
    
    borders_xml = f'''
        <w:tcBorders {nsdecls("w")}>
            {border_tag("top", top)}
            {border_tag("left", left)}
            {border_tag("bottom", bottom)}
            {border_tag("right", right)}
        </w:tcBorders>
    '''
    cell._tc.get_or_add_tcPr().append(parse_xml(borders_xml))

# Expanded Keywords for Lab 03
KEYWORDS = {
    'clc', 'clear', 'close', 'all', 'hold', 'on', 'off', 'grid', 'figure', 
    'if', 'else', 'elseif', 'end', 'for', 'while', 'return', 'function', 'break', 'tic', 'toc'
}
BUILTINS = {
    'linspace', 'cos', 'sin', 'exp', 'stem', 'plot', 'xlabel', 'ylabel', 
    'title', 'legend', 'subplot', 'sgtitle', 'xlim', 'ylim', 'ones', 
    'size', 'ceil', 'floor', 'double', 'abs', 'real', 'imag', 'trapz', 
    'fprintf', 'max', 'isfinite', 'diff', 'length', 'randi', 'zeros', 
    'disp', 'class', 'uint8', 'uint16', 'uint32', 'int8', 'int32', 'single', 'rng'
}

def highlight_matlab_code_in_cell(cell, code_text):
    C_KEYWORD = RGBColor(0, 0, 255)      # Blue
    C_BUILTIN = RGBColor(0, 110, 140)    # Teal / Deep Cyan
    C_STRING  = RGBColor(163, 21, 21)    # Red/Maroon
    C_COMMENT = RGBColor(34, 139, 34)    # Forest Green
    C_NUMBER  = RGBColor(128, 0, 128)    # Purple
    C_DEFAULT = RGBColor(30, 30, 30)     # Dark

    lines = code_text.strip().split('\n')
    for line in lines:
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.line_spacing = Pt(12)
        
        token_pattern = re.compile(
            r'(%.*$)|'                         
            r"('(?:''|[^'\n])*')|"             
            r'("(?:""|[^"\n])*")|'             
            r'(\b[A-Za-z_][A-Za-z0-9_]*\b)|'  
            r'(\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b)|' 
            r'(\s+)|'                          
            r'(.)'                             
        )
        
        for match in token_pattern.finditer(line):
            comment, str1, str2, word, num, space, other = match.groups()
            run = p.add_run()
            run.font.name = 'Consolas'
            run.font.size = Pt(9.5)
            
            if comment:
                run.text = comment
                run.font.color.rgb = C_COMMENT
            elif str1:
                run.text = str1
                run.font.color.rgb = C_STRING
            elif str2:
                run.text = str2
                run.font.color.rgb = C_STRING
            elif word:
                run.text = word
                if word in KEYWORDS:
                    run.font.color.rgb = C_KEYWORD
                    run.font.bold = True
                elif word in BUILTINS:
                    run.font.color.rgb = C_BUILTIN
                    run.font.bold = True
                else:
                    run.font.color.rgb = C_DEFAULT
            elif num:
                run.text = num
                run.font.color.rgb = C_NUMBER
            elif space:
                run.text = space
                run.font.color.rgb = C_DEFAULT
            elif other:
                run.text = other
                run.font.color.rgb = C_DEFAULT

def predict_output_type(code_text):
    """Predicts if the MATLAB code outputs a graph or text."""
    graph_keywords = ['plot(', 'hist(', 'figure', 'scatter(', 'bar(', 'imshow(', 'stem(']
    for kw in graph_keywords:
        if kw in code_text:
            return "Graph"
    return "Text"

def generate_lab_report():
    print("Generating beautifully formatted Lab 03 Report...")
    doc = docx.Document()

    # Page setup - Margins (0.8 inches on all sides)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # --- Document Header & Title ---
    header_p = doc.add_paragraph()
    header_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    header_p.paragraph_format.space_after = Pt(2)
    run_sub = header_p.add_run("DEPARTMENT OF AVIONICS ENGINEERING\nAVE 4510: MODELLING AND SIMULATION SESSIONAL")
    run_sub.font.name = 'Calibri'
    run_sub.font.size = Pt(11)
    run_sub.font.bold = True
    run_sub.font.color.rgb = COLOR_SECONDARY

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_after = Pt(16)
    run_title = title_p.add_run("LABORATORY REPORT 03\nLoops and Data Types")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(18)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_PRIMARY

    # Meta Table (Student & Course Info)
    info_table = doc.add_table(rows=2, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_table.autofit = False

    info_data = [
        [("Course Code & Title:", " AVE 4510: Modelling and Simulation"), ("Date of Performance:", " ______________________")],
        [("Lab Title:", " Lab 03 - Loops and Data Types"), ("Student Name / ID:", " Md. Rezwan Zani / 24024021")]
    ]

    for row_idx, row in enumerate(info_table.rows):
        for col_idx, cell in enumerate(row.cells):
            cell.width = Inches(3.4)
            set_cell_background(cell, HEX_PRIMARY_BG)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            set_cell_borders(cell, top="single", bottom="single", left="single", right="single", color="B0C4DE", sz="4")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            lbl, val = info_data[row_idx][col_idx]
            r1 = p.add_run(lbl)
            r1.font.name = 'Calibri'
            r1.font.size = Pt(9.5)
            r1.font.bold = True
            r1.font.color.rgb = COLOR_PRIMARY
            r2 = p.add_run(val)
            r2.font.name = 'Calibri'
            r2.font.size = Pt(9.5)
            r2.font.color.rgb = COLOR_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- Processing Files ---
    modules = {
        "Module 6": [
            "approx_sqrt.m", "BadBreak.m", "for_loop_example.m", "for_loop_variations.m",
            "GoodBreak.m", "GoodReturn.m", "logical_indexing.m", "norealloc.m",
            "possum.m", "prealloc.m", "sumintup.m", "timer_example.m"
        ],
        "Module 7": [
            "check_classes.m", "data_limits.m", "type_conversion.m"
        ]
    }

    topic_counter = 1

    for module_name, files in modules.items():
        # Add Module Heading
        mod_head = doc.add_paragraph()
        mod_head.paragraph_format.space_before = Pt(18)
        run_mod = mod_head.add_run(f"--- {module_name} ---")
        run_mod.font.name = 'Calibri'
        run_mod.font.size = Pt(14)
        run_mod.font.bold = True
        run_mod.font.color.rgb = COLOR_SECONDARY
        mod_head.alignment = WD_ALIGN_PARAGRAPH.CENTER

        for filename in files:
            filepath = os.path.join(module_name, filename)
            
            if not os.path.exists(filepath):
                print(f"Warning: Could not find {filepath}. Skipping.")
                continue
            
            with open(filepath, 'r', encoding='utf-8') as f:
                code_content = f.read()
                
            # Extract description
            topic_match = re.search(r'%\s*TOPIC:\s*(.*)', code_content, re.IGNORECASE)
            description = topic_match.group(1).strip() if topic_match else "No description provided."
            
            # Generate clean Topic Name
            clean_topic_name = filename.replace('.m', '').replace('_', ' ').title()
            expected_output = predict_output_type(code_content)

            # 1. Heading (Format: "Topic 01: Name")
            h_p = doc.add_paragraph()
            h_p.paragraph_format.space_before = Pt(14)
            h_p.paragraph_format.space_after = Pt(2)
            h_p.paragraph_format.keep_with_next = True
            
            r_num = h_p.add_run(f"Topic {topic_counter:02d}: ")
            r_num.font.name = 'Calibri'
            r_num.font.size = Pt(13)
            r_num.font.bold = True
            r_num.font.color.rgb = COLOR_PRIMARY
            
            r_t = h_p.add_run(clean_topic_name)
            r_t.font.name = 'Calibri'
            r_t.font.size = Pt(13)
            r_t.font.bold = True
            r_t.font.color.rgb = COLOR_SECONDARY

            # 2. Problem Statement / Description Box
            desc_table = doc.add_table(rows=1, cols=1)
            desc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
            desc_table.autofit = False
            c_desc = desc_table.rows[0].cells[0]
            c_desc.width = Inches(6.8)
            set_cell_background(c_desc, HEX_PRIMARY_BG)
            set_cell_margins(c_desc, top=80, bottom=80, left=120, right=120)
            set_cell_borders(c_desc, left="single", color="003366", sz="18")
            
            p_desc = c_desc.paragraphs[0]
            p_desc.paragraph_format.space_after = Pt(0)
            p_desc.paragraph_format.line_spacing = Pt(13)
            r_desc = p_desc.add_run(description)
            r_desc.font.name = 'Calibri'
            r_desc.font.size = Pt(10)
            r_desc.font.color.rgb = COLOR_TEXT

            # 3. Code Heading
            c_head = doc.add_paragraph()
            c_head.paragraph_format.space_before = Pt(8)
            c_head.paragraph_format.space_after = Pt(2)
            c_head.paragraph_format.keep_with_next = True
            r_ch = c_head.add_run("MATLAB Implementation Code:")
            r_ch.font.name = 'Calibri'
            r_ch.font.size = Pt(10.5)
            r_ch.font.bold = True
            r_ch.font.color.rgb = COLOR_PRIMARY

            # 4. Code Block with Syntax Highlighting
            code_table = doc.add_table(rows=1, cols=1)
            code_table.alignment = WD_TABLE_ALIGNMENT.CENTER
            code_table.autofit = False
            c_code = code_table.rows[0].cells[0]
            c_code.width = Inches(6.8)
            set_cell_background(c_code, HEX_CODE_BG)
            set_cell_margins(c_code, top=100, bottom=100, left=120, right=120)
            set_cell_borders(c_code, top="single", bottom="single", left="single", right="single", color="D0D5DD", sz="4")
            
            highlight_matlab_code_in_cell(c_code, code_content)

            # 5. Output Heading
            out_head = doc.add_paragraph()
            out_head.paragraph_format.space_before = Pt(8)
            out_head.paragraph_format.space_after = Pt(2)
            out_head.paragraph_format.keep_with_next = True
            
            heading_text = "Simulation Output Plot:" if expected_output == "Graph" else "Command Window Output:"
            r_oh = out_head.add_run(heading_text)
            r_oh.font.name = 'Calibri'
            r_oh.font.size = Pt(10.5)
            r_oh.font.bold = True
            r_oh.font.color.rgb = COLOR_PRIMARY

            # 6. Blank Output Box with dashed border
            out_table = doc.add_table(rows=1, cols=1)
            out_table.alignment = WD_TABLE_ALIGNMENT.CENTER
            out_table.autofit = False
            c_out = out_table.rows[0].cells[0]
            c_out.width = Inches(6.8)
            set_cell_background(c_out, HEX_BOX_BG)
            set_cell_margins(c_out, top=200, bottom=200, left=150, right=150)
            set_cell_borders(c_out, top="dashed", bottom="dashed", left="dashed", right="dashed", color="999999", sz="6")
            
            p_box = c_out.paragraphs[0]
            p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_box.paragraph_format.space_before = Pt(60) if expected_output == "Graph" else Pt(20)
            p_box.paragraph_format.space_after = Pt(60) if expected_output == "Graph" else Pt(20)
            
            placeholder_text = "[ Insert Output Plot Image Here ]" if expected_output == "Graph" else "[ Paste Command Window Output Here ]"
            r_ph = p_box.add_run(placeholder_text)
            r_ph.font.name = 'Calibri'
            r_ph.font.size = Pt(10.5)
            r_ph.font.italic = True
            r_ph.font.color.rgb = COLOR_MUTED

            spacer = doc.add_paragraph()
            spacer.paragraph_format.space_after = Pt(8)
            
            topic_counter += 1

    output_filename = "Lab_03_Report_Final.docx"
    doc.save(output_filename)
    print(f"\nReport successfully generated: {output_filename}")

if __name__ == "__main__":
    generate_lab_report()