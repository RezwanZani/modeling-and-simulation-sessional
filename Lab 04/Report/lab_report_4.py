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

# --- Core Styling Helpers ---
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

# --- MATLAB Syntax Highlighting ---
KEYWORDS = {
    'clc', 'clear', 'close', 'all', 'hold', 'on', 'off', 'grid', 'figure', 
    'if', 'else', 'elseif', 'end', 'for', 'while', 'return', 'function', 'break'
}
BUILTINS = {
    'linspace', 'cos', 'sin', 'exp', 'stem', 'plot', 'xlabel', 'ylabel', 
    'title', 'legend', 'subplot', 'sgtitle', 'xlim', 'ylim', 'ones', 
    'size', 'ceil', 'floor', 'double', 'abs', 'real', 'imag', 'trapz', 
    'fprintf', 'disp', 'max', 'isfinite', 'diff', 'length', 'polyfit'
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

# --- Lab 04 Data ---
lab_data = [
    {
        "type": "theory",
        "title": "Topic 1: What is Computational Science?",
        "desc": "• Real-world systems are often too large, expensive, dangerous, or complicated to study directly (e.g., hurricanes, drug testing on humans, aircraft physical testing).\n• Scientists create computer-based models to study virtual versions of these systems and observe their behavior.\n• It combines computer technology, mathematical methods, and scientific principles to solve complex problems.\n• Examples include weather prediction, aircraft design, climate change study, and tracking disease spread."
    },
    {
        "type": "theory",
        "title": "Topic 2: Traditional Scientific Approach",
        "desc": "Historically depended on the scientific method, which involves three main steps:\n• Theory Development: Creating an explanation for a natural phenomenon.\n• Experimentation: Performing tests to check if the theory is correct.\n• Observation and Analysis: Observing results and analyzing relationships between factors."
    },
    {
        "type": "theory",
        "title": "Topic 3: From Scientific Discoveries to Mathematical Models",
        "desc": "• A mathematical model represents a system's behavior using a set of equations or mathematical relationships.\n• It provides an approximate representation of the important features rather than copying reality perfectly."
    },
    {
        "type": "theory",
        "title": "Topic 4: Why Do We Need Computer Models?",
        "desc": "• Equations become too complex for humans to solve manually due to thousands of variables, massive amounts of data, and complicated interactions.\n• The process sequence flows from: Real-world system → Scientific understanding → Mathematical equations → Computer program → Simulation results."
    },
    {
        "type": "theory",
        "title": "Topic 5: Simulation: Meaning and Importance",
        "desc": "• Simulation is the process of using a computer model to imitate the behavior of a real-world system.\n• It allows researchers to test ideas safely, predict future situations, reduce cost, and save time.\n• Programming environments like MATLAB and Python are commonly used."
    },
    {
        "type": "theory",
        "title": "Topic 6: Computational Modeling in Aeronautics",
        "desc": "• Transformed aircraft design from physical wind tunnel testing to computer simulations of airflow, wing performance, and structural behavior before building the actual aircraft.\n• Developed from early-stage 2D airflow simulation over wings to advanced-stage 3D simulations of complete aircraft designs."
    },
    {
        "type": "theory",
        "title": "Topic 7: Understanding the Concept of a Model",
        "desc": "A model is an abstraction or simplification of a real-world object or phenomenon.\nTypes of Models:\n• Physical Model: A physical representation (e.g., clay car prototypes or river scale models).\n• Mathematical Model: Representation using equations developed through theory and experimentation.\n• Computer Model: A mathematical model implemented using computer programming code."
    },
    {
        "type": "theory",
        "title": "Topic 8: Complete Modeling Process Flowchart Steps",
        "desc": "• The overall process involves: Analyze problem and define objectives, create conceptual model, make simplifying assumptions, choose variables, define relationships, create equations, implement computer model, verify results, validate model, analyze results, and improve/refine the model.\n• Verification vs. Validation: Verification answers \"Did we build the model correctly?\" (checking code and calculations). Validation answers \"Did we build the correct model?\" (comparing it against real experiments and field data)."
    },
    {
        "type": "theory",
        "title": "Topic 9: Model Classifications",
        "desc": "• Deterministic vs. Probabilistic: Deterministic models have no randomness and produce a fixed output for a given input. Probabilistic models include randomness where different runs produce different results.\n• Static vs. Dynamic: Static models study a system at one fixed condition. Dynamic models study how a system changes over time.\n• Continuous vs. Discrete: Continuous models track time changing continuously. Discrete models divide time into small, distinct steps."
    },
    {
        "type": "theory",
        "title": "Topic 10: Deterministic Linear Models",
        "desc": "• Used because many real-world systems can be approximated using linear relationships (constant slope, straight line, predictable change).\n• Examples include truck loading weight, spring deformation (Hooke's Law), electrical resistance (Ohm's Law), and data interpolation."
    },
    {
        "type": "code",
        "title": "Practice Problem 1: Aircraft Fuel Consumption Prediction Model",
        "desc": "Details: An aircraft Flight Management System (FMS) needs to estimate fuel remaining where consumption is linear with flight time.\nMathematical Model: F(t) = F_0 - rt where F_0 = 12,000 kg (initial fuel) and r = 250 kg/hour (consumption rate).\nTasks: Calculate remaining fuel after 5, 10, and 20 hours, generate a graph, and find when fuel reaches 2,000 kg.",
        "code": r"""clc; clear;
% Aircraft parameters 
initialFuel = 12000;
consumptionRate = 250;

% Flight time
t = 0:1:40;

% Linear fuel model
fuelRemaining = initialFuel - consumptionRate*t;

% Display selected values 
time = [5 10 20];
fuel = initialFuel - consumptionRate*time;

disp("Flight Time (hours)");
disp(time);
disp("Remaining Fuel (kg)");
disp(fuel);

% Find time when fuel reaches 2000 kg 
requiredFuel = 2000;
flightTime = (initialFuel-requiredFuel)/consumptionRate;
fprintf("Fuel reaches 2000 kg after %.2f hours\n", flightTime);

% Plot
plot(t, fuelRemaining, 'LineWidth', 2);
xlabel('Flight Time (hours)');
ylabel('Remaining Fuel (kg)');
title('Aircraft Fuel Consumption Linear Model');
grid on;""",
        "output_type": "Graph & Text Output"
    },
    {
        "type": "code",
        "title": "Practice Problem 2: Aircraft Altitude Sensor Calibration Model",
        "desc": "Details: An aircraft's pressure altitude sensor changes voltage output linearly with altitude.\nMathematical Model: V = mH + c where V is sensor voltage, H is altitude, m is sensitivity coefficient, and c is the initial offset voltage. Given points: (0m, 0.5V) and (4000m, 5.7V), yielding V = 0.0013H + 0.5.\nTasks: Determine linear calibration equation, estimate sensor voltage at 2500m, 3500m, and 5000m, and plot altitude vs voltage.",
        "code": r"""clc; clear;
% Calibration data
Altitude = [0 1000 2000 3000 4000];
Voltage = [0.5 1.8 3.1 4.4 5.7];

% Linear fitting
model = polyfit(Altitude, Voltage, 1);
m = model(1);
c = model(2);

fprintf("Calibration Equation:\n");
fprintf("V = %.4fH + %.2f\n", m, c);

% Predict voltage
newAltitude = [2500 3500 5000];
predictedVoltage = m*newAltitude + c;
disp("Altitude");
disp(newAltitude);
disp("Voltage");
disp(predictedVoltage);

% Plot
plot(Altitude, Voltage, 'o');
hold on;
plot(newAltitude, predictedVoltage, '*');
xlabel("Altitude (m)");
ylabel("Sensor Voltage (V)");
title("Altitude Sensor Calibration Model");
grid on;""",
        "output_type": "Graph & Text Output"
    },
    {
        "type": "code",
        "title": "Practice Problem 3: Aircraft Communication System Signal Attenuation Model",
        "desc": "Details: Signal strength loss decreases linearly as the distance between the aircraft and the ground station increases.\nMathematical Model: S(d) = S_0 - kd where S(d) is received signal strength (dBm), S_0 is initial strength (-20 dBm), k is the attenuation coefficient (0.3), and d is distance (km).\nTasks: Create a linear attenuation model, predict signal strength at 250km, 300km, and 400km, find maximum communication range when strength reaches -100 dBm, and plot signal loss vs distance.",
        "code": r"""clc; clear;
% Communication data
distance = [0 50 100 150 200]; 
signal = [-20 -35 -50 -65 -80];

% Linear model
model = polyfit(distance, signal, 1);
k = model(1);
S0 = model(2);

fprintf("Signal Model:\n");
fprintf("S = %.3fd + %.2f\n", k, S0);

% Prediction
newDistance = [250 300 400];
predictedSignal = k*newDistance + S0;
disp("Distance");
disp(newDistance);
disp("Signal Strength");
disp(predictedSignal);

% Find communication limit
limit = -100;
range = (limit - S0)/k;
fprintf("Maximum communication range = %.2f km\n", range);

% Plot
plot(distance, signal, 'o');
hold on;
plot(newDistance, predictedSignal, '*');
xlabel("Distance (km)");
ylabel("Signal Strength (dBm)");
title("Aircraft Communication Signal Attenuation"); 
grid on;""",
        "output_type": "Graph & Text Output"
    }
]

def generate_lab_report():
    print("Generating beautifully formatted Lab 04 Report...")
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
    run_title = title_p.add_run("LABORATORY REPORT 04\nIntroduction to Computational Modeling")
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
        [("Lab Title:", " Lab 04 - Computational Modeling Intro"), ("Student Name / ID:", " Md. Rezwan Zani / 24024021")]
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

    # --- Process Embedded Data ---
    for item in lab_data:
        # 1. Heading (Title)
        h_p = doc.add_paragraph()
        h_p.paragraph_format.space_before = Pt(14)
        h_p.paragraph_format.space_after = Pt(2)
        h_p.paragraph_format.keep_with_next = True
        
        r_t = h_p.add_run(item['title'])
        r_t.font.name = 'Calibri'
        r_t.font.size = Pt(13)
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_PRIMARY

        # 2. Description Box
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
        r_desc = p_desc.add_run(item['desc'])
        r_desc.font.name = 'Calibri'
        r_desc.font.size = Pt(10)
        r_desc.font.color.rgb = COLOR_TEXT

        # If item has code, generate code and output blocks
        if item['type'] == 'code':
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
            
            highlight_matlab_code_in_cell(c_code, item['code'])

            # 5. Output Heading
            out_head = doc.add_paragraph()
            out_head.paragraph_format.space_before = Pt(8)
            out_head.paragraph_format.space_after = Pt(2)
            out_head.paragraph_format.keep_with_next = True
            
            r_oh = out_head.add_run(f"Simulation Output ({item['output_type']}):")
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
            p_box.paragraph_format.space_before = Pt(80) 
            p_box.paragraph_format.space_after = Pt(80) 
            
            r_ph = p_box.add_run("[ Insert Output Plot Image & Command Window Output Here ]")
            r_ph.font.name = 'Calibri'
            r_ph.font.size = Pt(10.5)
            r_ph.font.italic = True
            r_ph.font.color.rgb = COLOR_MUTED

        spacer = doc.add_paragraph()
        spacer.paragraph_format.space_after = Pt(8)

    output_filename = "Lab_04_Report_Final.docx"
    doc.save(output_filename)
    print(f"\nReport successfully generated: {output_filename}")

if __name__ == "__main__":
    generate_lab_report()