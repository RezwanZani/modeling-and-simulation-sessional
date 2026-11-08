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
    'fprintf', 'disp', 'max', 'isfinite', 'diff', 'length', 'polyfit',
    'ode45', 'log', 'find', 'isempty', 'yline', 'text', 'round', 'sprintf'
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

# --- Lab 05 Data ---
lab_data = [
    {
        "type": "code",
        "title": "Problem 1: Aircraft Battery Discharge Model (Exponential Decay)",
        "desc": "Problem Statement: An aircraft UAV uses a lithium-ion battery during flight. The battery capacity decreases exponentially: C(t) = C_0 * e^(-kt) where C(t) is remaining capacity, C_0 = 100% (initial), k = 0.08 (discharge constant), and t = flight time.\nTasks: Plot battery capacity for 0-10 hours. Determine remaining battery percentage after 5 hours. Find the time when battery capacity reaches 20%.",
        "code": r"""clc; clear; close all;

% Aircraft Battery Discharge Model (Exponential Decay)
initial_capacity = 100;  % Initial battery capacity (%)
discharge_rate = 0.08;   % Discharge constant (k)

% Flight time vector (0 to 10 hours)
t = linspace(0, 10, 100); 

% Exponential decay equation
capacity = initial_capacity * exp(-discharge_rate * t);

% Plotting the decay curve
figure('Name', 'Battery Discharge Model');
plot(t, capacity, 'b', 'LineWidth', 2.5);
grid on;
xlabel('Time in Flight (hours)');
ylabel('Capacity Remaining (%)');
title('UAV Battery Discharge Over Time');

% Calculate capacity at specific time (t = 5 hrs)
t_eval = 5;
cap_at_5 = initial_capacity * exp(-discharge_rate * t_eval);
fprintf('Battery remaining at 5 hours: %.2f%%\n', cap_at_5);

% Calculate time when capacity hits 20%
target_cap = 20;
t_target = -log(target_cap / initial_capacity) / discharge_rate;
fprintf('Time to reach 20%% capacity: %.2f hours\n', t_target);

% Mark data points on the plot
hold on;
plot(t_eval, cap_at_5, 'ms', 'MarkerSize', 8, 'MarkerFaceColor', 'm');
text(t_eval, cap_at_5 + 5, sprintf(' %.1f%% (5hr)', cap_at_5));

plot(t_target, target_cap, 'ks', 'MarkerSize', 8, 'MarkerFaceColor', 'k');
text(t_target, target_cap + 5, sprintf(' 20%% (%.1fhr)', t_target));
hold off;""",
        "output_type": "Graph & Text Output"
    },
    {
        "type": "code",
        "title": "Problem 2: UAV Population-Based Drone Fleet Growth Model (Logistic Growth)",
        "desc": "Problem Statement: A company operates delivery drones. Initial population is P_0 = 50. Maximum fleet size is K = 1000 due to constraints. The growth follows a logistic differential equation with rate r = 0.4.\nTasks: Using MATLAB, simulate fleet growth for 20 years, plot drone population versus time, and compare logistic growth with unlimited exponential growth.",
        "code": r"""clc; clear; close all;

% UAV Fleet Growth Model: Logistic vs Exponential
pop_initial = 50;    % Starting number of drones
max_capacity = 1000; % Maximum fleet capacity (K)
growth_rate = 0.4;   % Rate of growth (r)

time_yrs = 0:0.2:20; % Simulation over 20 years

% Compute Logistic Growth
P_log = max_capacity ./ (1 + ((max_capacity - pop_initial)/pop_initial) .* exp(-growth_rate .* time_yrs));

% Compute Unlimited Exponential Growth
P_exp = pop_initial .* exp(growth_rate .* time_yrs);

% Generate Comparison Plot
figure('Name', 'Drone Population Growth');
plot(time_yrs, P_log, 'g', 'LineWidth', 2.5);
hold on;
plot(time_yrs, P_exp, 'r-.', 'LineWidth', 2);
grid on;

xlabel('Time (Years)');
ylabel('Fleet Size (Number of Drones)');
title('UAV Fleet Expansion: Restricted vs Unrestricted');
legend('Logistic (Cap: 1000)', 'Exponential (Unlimited)', 'Location', 'northwest');

% Output final populations at t = 20
t_final = 20;
final_logistic = max_capacity / (1 + ((max_capacity - pop_initial)/pop_initial) * exp(-growth_rate * t_final));
final_exponential = pop_initial * exp(growth_rate * t_final);

fprintf('--- 20 Year Projection ---\n');
fprintf('Logistic Model Output: %d drones\n', round(final_logistic));
fprintf('Exponential Model Output: %d drones\n', round(final_exponential));""",
        "output_type": "Graph & Text Output"
    },
    {
        "type": "code",
        "title": "Problem 3: Aircraft Autopilot Temperature Control System (Feedback Model)",
        "desc": "Problem Statement: An aircraft environmental control system maintains cabin temperature. Desired temperature is 20°C, initial is 30°C. The system uses negative feedback: dT/dt = -k(T - T_desired) with k=0.5.\nTasks: Simulate cabin temperature for 20 minutes using ODE45, plot the temperature response, and determine how quickly the system reaches 20°C (within tolerance).",
        "code": r"""clc; clear; close all;

% Aircraft Cabin Temperature Control (Negative Feedback)
T_target = 20;       % Setpoint temperature (C)
T_initial = 30;      % Starting temperature (C)
feedback_gain = 0.5; % Proportional control constant (k)

% Run simulation for 20 minutes
t_range = [0 20]; 

% Solve the differential equation with ode45
[time_sim, Temp_sim] = ode45(@(t, T) temp_dynamics(t, T, feedback_gain, T_target), t_range, T_initial);

% Plotting the system response
figure('Name', 'Cabin Temp Control');
plot(time_sim, Temp_sim, 'b', 'LineWidth', 2);
hold on;
yline(T_target, 'r--', 'LineWidth', 1.5); % Draw target line
grid on;

xlabel('Simulation Time (mins)');
ylabel('Temperature (Celsius)');
title('Cabin Temperature Feedback Regulation');
legend('System Response', 'Target Setpoint');

% Identify when temperature reaches within 0.1C of target
tol = 0.1; 
idx_reached = find(abs(Temp_sim - T_target) < tol, 1);

if ~isempty(idx_reached)
    fprintf('Target achieved (~%.1fC) at %.2f minutes.\n', T_target, time_sim(idx_reached));
else
    fprintf('Target not reached within simulation time.\n');
end

% Define the ODE function
function dT_dt = temp_dynamics(~, T, k, T_set)
    % Rate of change depends on the error (T - T_set)
    dT_dt = -k * (T - T_set);
end""",
        "output_type": "Graph & Text Output"
    },
    {
        "type": "code",
        "title": "Problem 4: Aircraft Altitude Control System With Nonlinear Dynamics",
        "desc": "Problem Statement: A small UAV altitude controller is modeled with nonlinear dynamics involving vertical velocity, gravity, upward thrust, and a nonlinear drag force (c*v*|v|).\nTasks: Simulate UAV motion for 20 seconds using ODE45. Plot altitude versus time and compare the flight trajectory between 'Without drag' and 'With nonlinear drag'.",
        "code": r"""clc; clear; close all;

% UAV Altitude Controller (Nonlinear Dynamics)
gravity = 9.81;    % Gravity acceleration (m/s^2)
drag_coeff = 0.05; % Nonlinear drag constant (c)
thrust_cmd = 15.0; % Upward thrust (u)

% Initial State: [Altitude; Velocity]
state_0 = [0; 0]; 

sim_time = [0 20]; % 20 seconds simulation

% Solve ODE with Nonlinear Drag
[t_drag, state_drag] = ode45(@(t, x) uav_dynamics(t, x, thrust_cmd, gravity, drag_coeff), sim_time, state_0);
alt_drag = state_drag(:, 1);
vel_drag = state_drag(:, 2);

% Solve ODE Without Drag (c = 0)
[t_nodrag, state_nodrag] = ode45(@(t, x) uav_dynamics(t, x, thrust_cmd, gravity, 0), sim_time, state_0);
alt_nodrag = state_nodrag(:, 1);

% Plot 1: Altitude Comparison
figure('Name', 'Altitude Tracking');
plot(t_drag, alt_drag, 'b', 'LineWidth', 2);
hold on;
plot(t_nodrag, alt_nodrag, 'r--', 'LineWidth', 2);
grid on;
xlabel('Time (s)');
ylabel('Altitude (m)');
title('UAV Altitude: Drag vs No Drag');
legend('With Aerodynamic Drag', 'Ideal (No Drag)', 'Location', 'northwest');

% Plot 2: Velocity Profile
figure('Name', 'Velocity Profile');
plot(t_drag, vel_drag, 'g', 'LineWidth', 2);
grid on;
xlabel('Time (s)');
ylabel('Vertical Speed (m/s)');
title('UAV Climb Velocity (With Drag)');

% Dynamics Function Definition
function dx_dt = uav_dynamics(~, state, u, g, c)
    h = state(1); % current altitude
    v = state(2); % current velocity
    
    h_dot = v;
    v_dot = u - g - (c * v * abs(v)); % nonlinear drag term
    
    dx_dt = [h_dot; v_dot];
end""",
        "output_type": "Graphs Output"
    }
]

def generate_lab_report():
    print("Generating beautifully formatted Lab 05 Report...")
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
    run_title = title_p.add_run("LABORATORY REPORT 05\nDynamic System Modeling & ODEs")
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
        [("Lab Title:", " Lab 05 - Dynamic System Modeling"), ("Student Name / ID:", " Md. Rezwan Zani / 24024021")]
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

    output_filename = "Lab_05_Report_Final.docx"
    doc.save(output_filename)
    print(f"\nReport successfully generated: {output_filename}")

if __name__ == "__main__":
    generate_lab_report()