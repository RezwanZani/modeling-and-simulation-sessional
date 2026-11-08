import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import re

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

def set_cell_borders(cell, top="none", bottom="none", left="none", right="none", 
                     color="CCCCCC", sz="4"):
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

# MATLAB Keywords and Built-in Functions
KEYWORDS = {
    'clc', 'clear', 'close', 'all', 'hold', 'on', 'off', 'grid', 'figure', 
    'if', 'else', 'elseif', 'end', 'for', 'while', 'return', 'function'
}
BUILTINS = {
    'linspace', 'cos', 'sin', 'exp', 'stem', 'plot', 'xlabel', 'ylabel', 
    'title', 'legend', 'subplot', 'sgtitle', 'xlim', 'ylim', 'ones', 
    'size', 'ceil', 'floor', 'double', 'abs', 'real', 'imag', 'trapz', 
    'fprintf', 'max', 'isfinite', 'diff', 'zeros', 'randn', 'length', 'round'
}

def highlight_matlab_code_in_cell(cell, code_text):
    C_KEYWORD = RGBColor(0, 0, 255)      # Blue
    C_BUILTIN = RGBColor(0, 110, 140)    # Teal / Deep Cyan
    C_STRING  = RGBColor(163, 21, 21)    # Red/Maroon
    C_COMMENT = RGBColor(34, 139, 34)    # Forest Green
    C_NUMBER  = RGBColor(128, 0, 128)    # Purple
    C_DEFAULT = RGBColor(30, 30, 30)     # Dark

    lines = code_text.strip().split('\n')
    for line_idx, line in enumerate(lines):
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

# --- Document Header & Title ---
header_p = doc.add_paragraph()
header_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
header_p.paragraph_format.space_after = Pt(2)
run_sub = header_p.add_run("DEPARTMENT OF AVIONICS ENGINEERING\nAVE 4502: SIGNALS AND SYSTEMS SESSIONAL")
run_sub.font.name = 'Calibri'
run_sub.font.size = Pt(11)
run_sub.font.bold = True
run_sub.font.color.rgb = COLOR_SECONDARY

title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
title_p.paragraph_format.space_after = Pt(16)
run_title = title_p.add_run("LABORATORY REPORT 02\nSystem Properties Analysis using MATLAB")
run_title.font.name = 'Calibri'
run_title.font.size = Pt(18)
run_title.font.bold = True
run_title.font.color.rgb = COLOR_PRIMARY

# Meta Table (Student & Course Info)
info_table = doc.add_table(rows=2, cols=2)
info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
info_table.autofit = False

info_data = [
    [("Course Code & Title:", " AVE 4502: Signals and Systems Sessional"), ("Student Name:", " Md. Rezwan Zani")],
    [("Lab Title:", " Lab 02 - System Properties"), ("Student ID:", " 24024021")]
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

# Exercises Definitions
exercises = [
    {
        "num": "Exercise 01",
        "title": "Continuous-Time Differentiator System",
        "desc": "A differentiator system is a system in which the output is proportional to the time derivative of the input. Consider a differentiator system described by the input–output relationship y(t) = dx(t)/dt, where x(t) is the applied input signal and y(t) is the output signal. Determine if this system is:\n\n"
                "(a) Linear or nonlinear, (b) Causal or non-causal, (c) Static or dynamic, (d) Time invariant or time variant, (e) Stable or unstable, (f) Invertible or not invertible.",
        "code": r"""% EXERCISE 01: Dynamic Continuous-Time System Analyzer
clc; clear; close all;

%% 1. Setup & System Definition
fs = 1000;          % Sampling frequency
dt = 1/fs;          % Time step
t = 0:dt:2;         % Time vector from 0 to 2 seconds
N = length(t);      % Number of samples
tol = 1e-6;         % Error tolerance for floating-point math

% Define the System Equation HERE. 
% Currently set to Differentiator: y(t) = dx(t)/dt
sys = @(x) [0, diff(x)/dt]; 

fprintf('--- EXERCISE 1: CONTINUOUS-TIME SYSTEM ANALYSIS ---\n\n');

%% (a) Linearity Test
x1 = sin(2*pi*2*t);
x2 = sin(2*pi*5*t);
a = 2; b = 3;

% Test superposition: sys(a*x1 + b*x2) == a*sys(x1) + b*sys(x2)
y_combo = sys(a*x1 + b*x2);
y_sum = a*sys(x1) + b*sys(x2);
linear_error = max(abs(y_combo - y_sum));

fprintf('(a) Linearity: ');
if linear_error < tol
    fprintf('LINEAR (Error: %e)\n', linear_error);
else
    fprintf('NONLINEAR (Error: %e)\n', linear_error);
end

%% (b) Causality Test
n0 = round(N/2);
xA = zeros(1,N); xB = zeros(1,N);
% Identical past
xA(1:n0) = sin(2*pi*3*t(1:n0));
xB(1:n0) = xA(1:n0);
% Different future
xA(n0+1:end) = 0;
xB(n0+1:end) = randn(1, N-n0);

yA = sys(xA); yB = sys(xB);
causal_error = max(abs(yA(1:n0) - yB(1:n0)));

fprintf('(b) Causality: ');
if causal_error < tol
    fprintf('CAUSAL (Output matched in identical past)\n');
else
    fprintf('NON-CAUSAL (Future input affected past output)\n');
end

%% (c) Static or Dynamic (Memory Test)
k = round(N/2);
xc1 = zeros(1,N); xc2 = zeros(1,N);
% Same current input, different previous input
xc1(k) = 0; xc2(k) = 0;
xc1(k-1) = 0; xc2(k-1) = 1;

yc1 = sys(xc1); yc2 = sys(xc2);
memory_diff = abs(yc1(k) - yc2(k));

fprintf('(c) Memory: ');
if memory_diff > tol
    fprintf('DYNAMIC / HAS MEMORY (Output changed based on past input)\n');
else
    fprintf('STATIC / MEMORYLESS\n');
end

%% (d) Time-Invariance Test
xTI = randn(1,N); xTI(1) = 0;
k_shift = 150;

y_original = sys(xTI);
% Shift input, then apply system
x_shifted = [zeros(1, k_shift), xTI(1:end-k_shift)];
y_from_shifted_input = sys(x_shifted);
% Apply system, then shift output
y_shifted_output = [zeros(1, k_shift), y_original(1:end-k_shift)];

ti_error = max(abs(y_from_shifted_input - y_shifted_output));

fprintf('(d) Time Invariance: ');
if ti_error < tol
    fprintf('TIME INVARIANT\n');
else
    fprintf('TIME VARIANT\n');
end

%% (e) Stability Test (BIBO)
% Bounded step input
u_step = double(t >= 0.5); 
y_step = sys(u_step);
% If max output is massively larger than max input (e.g. 50x), it's unstable
stability_ratio = max(abs(y_step)) / max(abs(u_step));

fprintf('(e) Stability: ');
if stability_ratio > 50 
    fprintf('UNSTABLE (Bounded input caused unbounded/massive output spike)\n');
else
    fprintf('STABLE (Output remained strictly bounded)\n');
end

%% (f) Invertibility Test
% Check if two different inputs yield the same output (many-to-one mapping)
x_inv1 = sin(2*pi*2*t);
x_inv2 = x_inv1 + 5; % Shifted by a constant

y_inv1 = sys(x_inv1);
y_inv2 = sys(x_inv2);
inv_output_diff = max(abs(y_inv1 - y_inv2));
inv_input_diff = max(abs(x_inv1 - x_inv2));

fprintf('(f) Invertibility: ');
if inv_output_diff < tol && inv_input_diff > tol
    fprintf('NOT INVERTIBLE (Different inputs produced identical outputs)\n\n');
else
    fprintf('INVERTIBLE (One-to-one mapping detected for test case)\n\n');
end

%% Plotting Logic (Input vs Output & Stability Proof)
figure('Name', 'Continuous System Logic Analysis');
subplot(2,1,1);
plot(t, x1, 'k', 'DisplayName', 'Input x(t)'); hold on;
plot(t, sys(x1), 'r--', 'LineWidth', 1.5, 'DisplayName', 'System Output y(t)');
grid on; xlabel('Time (s)'); ylabel('Amplitude'); title('System Response to Sine Wave'); legend;

subplot(2,1,2);
plot(t, u_step, 'k', 'DisplayName', 'Bounded Step Input'); hold on;
plot(t, y_step, 'r', 'DisplayName', 'System Output');
grid on; xlabel('Time (s)'); ylabel('Amplitude'); title('BIBO Stability Test'); legend;""",
        "output_label": "Output Plot 01: Continuous System Logic Analysis (exercise_1.png)"
    },
    {
        "num": "Exercise 02",
        "title": "Discrete-Time Difference System",
        "desc": "A discrete-time system is described by the input–output relationship y[n] = x[n] − x[n−1]. Determine if the system is:\n\n"
                "(a) Linear or nonlinear, (b) Causal or non-causal, (c) Static or dynamic, (d) Shift invariant or shift variant.",
        "code": r"""% EXERCISE 02: Dynamic Discrete-Time System Analyzer
clc; clear; close all;

%% 1. Setup & System Definition
N = 50;           % Number of samples
n = 0:N-1;        % Discrete time index
tol = 1e-9;       % Error tolerance

% Define the Discrete System Equation HERE. 
% Currently set to First-Difference: y[n] = x[n] - x[n-1]
sys = @(x) [x(1), diff(x)]; 

fprintf('--- EXERCISE 2: DISCRETE-TIME SYSTEM ANALYSIS ---\n\n');

rng(42);
x1 = randn(1, N);
x2 = randn(1, N);

%% (a) Linearity Test
a = 0.5; b = -1.5;
y_combo = sys(a*x1 + b*x2);
y_sum = a*sys(x1) + b*sys(x2);
linear_error = max(abs(y_combo - y_sum));

fprintf('(a) Linearity: ');
if linear_error < tol
    fprintf('LINEAR (Error: %e)\n', linear_error);
else
    fprintf('NONLINEAR (Error: %e)\n', linear_error);
end

%% (b) Causality Test
n0 = round(N/2);
xA = zeros(1,N); xB = zeros(1,N);
% Identical past
xA(1:n0) = sin(2*pi*5*(1:n0)/N);
xB(1:n0) = xA(1:n0);
% Different future
xA(n0+1:end) = 0;
xB(n0+1:end) = randn(1, N-n0);

yA = sys(xA); yB = sys(xB);
causal_error = max(abs(yA(1:n0) - yB(1:n0)));

fprintf('(b) Causality: ');
if causal_error < tol
    fprintf('CAUSAL (Output matched in identical past)\n');
else
    fprintf('NON-CAUSAL (Future input affected past output)\n');
end

%% (c) Static or Dynamic (Memory Test)
k = round(N/2);
xc1 = zeros(1,N); xc2 = zeros(1,N);
% Same current input, different previous input
xc1(k) = 0; xc2(k) = 0;
xc1(k-1) = 0; xc2(k-1) = 1;

yc1 = sys(xc1); yc2 = sys(xc2);
memory_diff = abs(yc1(k) - yc2(k));

fprintf('(c) Memory: ');
if memory_diff > tol
    fprintf('DYNAMIC / HAS MEMORY (Output changed based on past input)\n');
else
    fprintf('STATIC / MEMORYLESS\n');
end

%% (d) Shift-Invariance Test
k_shift = 5; 
y_original = sys(x1);

% Shift input then apply system
x1_shifted = [zeros(1, k_shift), x1(1:end-k_shift)];
y_from_shifted_input = sys(x1_shifted);

% Apply system then shift output
y_shifted_output = [zeros(1, k_shift), y_original(1:end-k_shift)];

shift_error = max(abs(y_from_shifted_input - y_shifted_output));

fprintf('(d) Shift Invariance: ');
if shift_error < tol
    fprintf('SHIFT INVARIANT (Error: %e)\n\n', shift_error);
else
    fprintf('SHIFT VARIANT (Error: %e)\n\n', shift_error);
end

%% Plotting Logic
figure('Name', 'Discrete System Logic Analysis');
subplot(2,1,1);
stem(n, x1, 'k', 'filled', 'DisplayName', 'Input x[n]'); hold on;
stem(n, sys(x1), 'r', 'DisplayName', 'Output y[n]');
grid on; xlabel('Sample n'); ylabel('Amplitude'); title('Discrete System Response'); legend;

subplot(2,1,2);
stem(n, y_from_shifted_input, 'b', 'filled', 'DisplayName', 'System applied to shifted input'); hold on;
stem(n, y_shifted_output, 'rX', 'MarkerSize', 8, 'DisplayName', 'Shift applied to system output');
grid on; xlabel('Sample n'); ylabel('Amplitude'); title('Shift Invariance Check (Visual Overlap)'); legend;""",
        "output_label": "Output Plot 02: Discrete Difference System Shift Invariance (exercise_2.png)"
    }
]

# Build Exercises into DOCX
for ex in exercises:
    # 1. Heading
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

    # 2. Problem Statement Box
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

    # 3. Code Heading
    c_head = doc.add_paragraph()
    c_head.paragraph_format.space_before = Pt(8)
    c_head.paragraph_format.space_after = Pt(2)
    c_head.paragraph_format.keep_with_next = True
    r_ch = c_head.add_run("MATLAB Implementation Code (Logic Evaluated & Printed to Console):")
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
    
    highlight_matlab_code_in_cell(c_code, ex['code'])

    # 5. Output Heading
    out_head = doc.add_paragraph()
    out_head.paragraph_format.space_before = Pt(8)
    out_head.paragraph_format.space_after = Pt(2)
    out_head.paragraph_format.keep_with_next = True
    r_oh = out_head.add_run("Simulation Output Plot:")
    r_oh.font.name = 'Calibri'
    r_oh.font.size = Pt(10.5)
    r_oh.font.bold = True
    r_oh.font.color.rgb = COLOR_PRIMARY

    # 6. Blank Output Box with dashed border for manual plot insertion
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
    p_box.paragraph_format.space_before = Pt(60)
    p_box.paragraph_format.space_after = Pt(60)
    r_ph = p_box.add_run(f"[ Insert Output Plot Image Here ]\n{ex['output_label']}")
    r_ph.font.name = 'Calibri'
    r_ph.font.size = Pt(10.5)
    r_ph.font.italic = True
    r_ph.font.color.rgb = COLOR_MUTED

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(8)

output_filename = "Lab_02_Signals_and_Systems_Report.docx"
doc.save(output_filename)
print(f"Report saved to: {output_filename}")