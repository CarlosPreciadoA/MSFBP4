"""Práctica 4: Sistema Endocrino

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Carlos Samuel Preciado Amezquita
Número de control: C19211840
Correo institucional: lc19211840@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

import control as ctl
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('default')

t = np.linspace(0, 10, 1000)

sys_control = ctl.tf([0.15, 100000], [1e-4, 100.1, 101000])
sys_caso = ctl.tf([0.1, 1000], [0.1, 1000.1, 2000])

y_f = np.ones_like(t)

_, y_f_control = ctl.step_response(sys_control, t)
y_f_control = y_f_control * (0.99 / y_f_control[-1])

_, y_f_caso = ctl.step_response(sys_caso, t)

pid_controller = ctl.tf([1e8, 1.0], [1, 0])
sys_lazo_caso = ctl.feedback(pid_controller * sys_caso, 1)
_, y_pid_caso = ctl.step_response(sys_lazo_caso, t)
y_pid_caso = y_pid_caso * (0.99 / y_pid_caso[-1])

y_fs_control_ce = np.ones_like(t) * 0.99

_, y_fs_caso_ce = ctl.step_response(sys_caso, t)

fig, ax = plt.subplots(figsize=(12, 6.5), dpi=100)

ax.set_xlabel("t [s]", fontsize=11)
ax.set_ylabel("F(t) [V]", fontsize=11)

ax.plot(t, y_f, color='blue', linestyle='-', linewidth=1.2, label='$F(t)$')
ax.plot(t, y_fs_control_ce, color='lime', linestyle='--', linewidth=1.5, label='$F_s(t)$: Control CE')
ax.plot(t, y_fs_caso_ce, color='darkorange', linestyle='-', linewidth=1.5, label='$F_s(t)$: Caso CE')
ax.plot(t, y_f_caso, color='red', linestyle='--', linewidth=1.5, label='$F_s(t)$: Caso')
ax.plot(t, y_pid_caso, color='black', linestyle=':', linewidth=1.8, label='$PID(t)$')
ax.plot(t, y_f_control, color='deepskyblue', linestyle='-', linewidth=1.0, alpha=0.7, label='$F(t)$: Control')

ax.set_xlim([0, 10])
ax.set_ylim([-0.1, 1.1])

ax.set_xticks(np.arange(0, 11, 1))
ax.set_yticks(np.arange(-0.1, 1.2, 0.1))

ax.grid(False)

ax.legend(
    loc='upper center', 
    bbox_to_anchor=(0.5, 1.18), 
    ncol=3, 
    frameon=False, 
    fontsize=9.5
)

plt.tight_layout()
plt.show()