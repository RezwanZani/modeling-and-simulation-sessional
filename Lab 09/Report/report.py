import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# Initialize document
doc = docx.Document()

# Page setup - Margins (0.8 inches on all sides)
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Color Palette Definitions
COLOR_PRIMARY = RGBColor(0, 51, 102)     # Deep Navy
COLOR_SECONDARY = RGBColor(70, 130, 180) # Steel Blue
COLOR_TEXT = RGBColor(40, 40, 40)        # Charcoal
COLOR_MUTED = RGBColor(120, 120, 120)    # Gray
HEX_PRIMARY_BG = "EBF3FA"
HEX_BOX_BG = "FAFAFA"

def set_cell_background(cell, fill_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f"""
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    """)
    tcPr.append(tcMar)

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", 
                     color="CCCCCC", sz="4"):
    def border_tag(side, val):
        if val == "none":
            return f'<w:{side} {nsdecls("w")} w:val="none"/>'
        return f'<w:{side} {nsdecls("w")} w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
    
    borders_xml = f"""
        <w:tcBorders {nsdecls("w")}>
            {border_tag("top", top)}
            {border_tag("left", left)}
            {border_tag("bottom", bottom)}
            {border_tag("right", right)}
        </w:tcBorders>
    """
    cell._tc.get_or_add_tcPr().append(parse_xml(borders_xml))

def add_dashed_box(doc, label):
    out_table = doc.add_table(rows=1, cols=1)
    out_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    out_table.autofit = False
    c_out = out_table.rows[0].cells[0]
    c_out.width = Inches(6.8)
    set_cell_background(c_out, HEX_BOX_BG)
    set_cell_margins(c_out, top=150, bottom=150, left=150, right=150)
    set_cell_borders(c_out, top="dashed", bottom="dashed", left="dashed", right="dashed", color="999999", sz="6")
    
    p_box = c_out.paragraphs[0]
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_before = Pt(40)
    p_box.paragraph_format.space_after = Pt(40)
    r_ph = p_box.add_run(f"[ Insert {label} Screenshot Here ]")
    r_ph.font.name = 'Calibri'
    r_ph.font.size = Pt(10.5)
    r_ph.font.italic = True
    r_ph.font.color.rgb = COLOR_MUTED

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(6)

# --- Document Header & Title ---
header_p = doc.add_paragraph()
header_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
header_p.paragraph_format.space_after = Pt(2)
run_sub = header_p.add_run("DEPARTMENT OF AVIONICS ENGINEERING\nAVE 4510: MODELLING AND SIMULATION")
run_sub.font.name = 'Calibri'
run_sub.font.size = Pt(11)
run_sub.font.bold = True
run_sub.font.color.rgb = COLOR_SECONDARY

title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_p.paragraph_format.space_after = Pt(16)
run_title = title_p.add_run("LABORATORY REPORT 09\nSimscape Electrical Circuit Simulations")
run_title.font.name = 'Calibri'
run_title.font.size = Pt(18)
run_title.font.bold = True
run_title.font.color.rgb = COLOR_PRIMARY

# Meta Table
info_table = doc.add_table(rows=2, cols=2)
info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
info_table.autofit = False

info_data = [
    [("Course Title:", " AVE 4510: Modelling and Simulation"), ("Date of Performance:", " 09 November 2026")],
    [("Lab Title:", " Lab 09"), ("Student Name / ID:", " Rezwan Shajib / _________________")]
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

exercises = [
    {
        "num": "Example 01",
        "title": "Simple DC Circuit Simulation",
        "desc": "Find voltages V1 and V2 in the simple DC circuit."
    },
    {
        "num": "Example 02",
        "title": "DC Circuit with Current Sources",
        "desc": "Calculate the node voltages in the given circuit using DC current sources."
    },
    {
        "num": "Example 03",
        "title": "Circuit with Dependent Source",
        "desc": "Find the current i0 in the circuit featuring a dependent voltage source."
    },
    {
        "num": "Example 04",
        "title": "Inverting Amplifier (Example 5.3)",
        "desc": "Calculate the output voltage vo and the current in the 10-kΩ resistor for the inverting op-amp circuit."
    },
    {
        "num": "Example 05",
        "title": "Op-Amp Circuit Analysis (Example 5.5)",
        "desc": "Calculate the output voltage vo for the given op-amp circuit with multiple DC sources."
    },
    {
        "num": "Example 06",
        "title": "Advanced Op-Amp Circuit (Example 5.6)",
        "desc": "Calculate vo and io in the given op-amp circuit using Simulink-PS components."
    },
    {
        "num": "Example 07",
        "title": "Op-Amp Integrator with Capacitor",
        "desc": "Sketch the output voltage for the circuit, given the triangular input voltage vi. Take vo = 0 at t = 0."
    }
]

# Build Exercises into DOCX
for ex in exercises:
    h_p = doc.add_paragraph()
    h_p.paragraph_format.space_before = Pt(14)
    h_p.paragraph_format.space_after = Pt(2)
    h_p.paragraph_format.keep_with_next = True
    
    r_num = h_p.add_run(f"{ex['num']}: ")
    r_num.font.name = 'Calibri'
    r_num.font.size = Pt(13)
    r_num.font.bold = True
    r_num.font.color.rgb = COLOR_PRIMARY
    
    r_t = h_p.add_run(ex['title'])
    r_t.font.name = 'Calibri'
    r_t.font.size = Pt(13)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_SECONDARY

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
    r_desc = p_desc.add_run(ex['desc'])
    r_desc.font.name = 'Calibri'
    r_desc.font.size = Pt(10)
    r_desc.font.color.rgb = COLOR_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 3 Placeholder Boxes for Simscape Models
    add_dashed_box(doc, "Question / Circuit Diagram")
    add_dashed_box(doc, "Simulink / Simscape Setup")
    add_dashed_box(doc, "Scope Graph / Output")

output_filename = "Lab_09_Modelling_Simulation_Report.docx"
doc.save(output_filename)
print(f"File generated successfully: {output_filename}")