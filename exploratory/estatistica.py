import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scienceplots
import shutil

# O Pandas já usa a vírgula como separador padrão e lê os cabeçalhos sozinhos
df = pd.read_csv("data_gravitational_confident.csv")

# O restante do código de análise permanece exatamente o mesmo!
max_final_mass = df['final_mass_source'].max()
min_final_mass = df['final_mass_source'].min()

shortname = df['shortName']

index_max = df['final_mass_source'].idxmax()
index_min = df['final_mass_source'].idxmin()

print(f"Evento com maior massa final: {df.loc[index_max, 'shortName']} = {max_final_mass}")
print(f"Evento com menor massa final: {df.loc[index_min, 'shortName']} = {min_final_mass}")


plt.style.use(['science'])

final_mass_source = df['final_mass_source']
mass_1_source = df['mass_1_source']
mass_2_source = df['mass_2_source']
chi_eff = df['chi_eff']
luminosity_distance = df['luminosity_distance']
chi_eff = df['chi_eff']


'''
#Disperção - Massa1 e Massa2
plt.figure(figsize=(8, 6))
plt.scatter(mass_1_source, mass_2_source, marker='o', s=50)
plt.axline((0, 0), slope=1, color='red', linewidth=2, linestyle='--', alpha=0.7, label="y = x")
plt.xlabel(r"Mass $1$ ($M_\odot$)", fontsize=25)
plt.ylabel(r"Mass $2$ ($M_\odot$)", fontsize=25)  # Alterado de xlabel para ylabel
plt.tick_params(axis='both', labelsize=15)
plt.savefig("mass1_x_mass2.png", dpi=300)
plt.show()
shutil.move('mass1_x_mass2.png', 'img_stat/mass1_x_mass2.png')

#Distancia vs Massa final
plt.figure(figsize=(8, 6))
plt.scatter(luminosity_distance, final_mass_source, marker='o', s=50)
plt.axline((0, 0), slope=0.01, color='red', linewidth=2, linestyle='--', alpha=0.7, label="y = x")
plt.axline((0, 0), slope=0.16, color='red', linewidth=2, linestyle='--', alpha=0.7, label="y = x")
plt.xlabel(r"Final Mass Source ($M_\odot$)", fontsize=25)
plt.ylabel(r"Luminosity Distance (Mpc)", fontsize=25)  # Alterado de xlabel para ylabel
plt.tick_params(axis='both', labelsize=15)
plt.savefig("distance_mass.png", dpi=300)
plt.show()
shutil.move('distance_mass.png', 'img_stat/distance_mass.png')


q_m1_m2 = mass_2_source/mass_1_source



# Configurando o tamanho da imagem
plt.figure(figsize=(8, 6))

# Criando o gráfico de densidade 2D
sns.kdeplot(
    x=chi_eff,           # Seu array do Spin Efetivo no eixo X
    y=q_m1_m2,                 # Seu array da Razão de Massa no eixo Y
    fill=True,           # Preenche os contornos com cor (estilo mapa de calor)
    thresh=0.02,         # Remove a cor de fundo onde a densidade é quase zero (limpa o gráfico)
    levels=10,           # Número de linhas de contorno/camadas
    cmap="mako"          # Paleta de cores (opções legais: 'viridis', 'plasma', 'mako', 'Blues')
)

# Customizando os eixos com a formatação matemática correta
plt.xlabel(r"Effective Spin ($\chi_{eff}$)", fontsize=25)
plt.ylabel(r"Mass Ratio ($q$)", fontsize=25)
plt.title(r"Joint Density Distribution: $\chi_{eff}$ vs $q$", fontsize=30)

# Adiciona uma grade sutil ao fundo
plt.grid(True, linestyle="--", alpha=0.5)
plt.savefig("join_q_chi_eff.png", dpi=300)
plt.show()
shutil.move('join_q_chi_eff.png', 'img_stat/join_q_chi_eff.png')





#Histogramas

#Final Mass
mean_sig = np.mean(final_mass_source)
stdg_sig = np.std(final_mass_source)
plt.figure(figsize=(8, 6))
plt.hist(final_mass_source, bins=15, color='skyblue', edgecolor='black')
plt.xlabel(r"Final Mass Source ($M_\odot$)", fontsize=25)
plt.ylabel("Frequency", fontsize = 25)
plt.title(rf'$\mu$ = {round(mean_sig,2)} $ M_\odot $,    $\sigma$ = {round(stdg_sig,2)} ', fontsize=30)
plt.tick_params(axis = 'both', labelsize=20)
plt.savefig("FinalMass.png", dpi=300)
plt.show()
shutil.move('FinalMass.png', 'img_stat/FinalMass.png')

#Mass1 and Mass2
mean1 = np.mean(mass_1_source)
mean2 = np.mean(mass_2_source)
stdg1 = np.std(mass_1_source)
stdg2 = np.std(mass_2_source)
plt.figure(figsize=(8, 6))
plt.hist(mass_1_source, bins=15, alpha=0.5, label=r'$m_1$', color='skyblue', edgecolor='black')
plt.hist(mass_2_source, bins=15, alpha=0.5, label=r'$m_2$', color='orange', edgecolor='black')
plt.xlabel(r"Mass Source ($M_\odot$)", fontsize=20)
plt.ylabel("Frequency", fontsize=20)
plt.legend(fontsize=15)
plt.title(rf'$\mu_1={mean1:.2f}, \sigma_1={stdg1:.2f} \quad | \quad '
          rf'\mu_2={mean2:.2f}, \sigma_2={stdg2:.2f} \quad [M_\odot]$', fontsize=18)
plt.tick_params(axis='both', labelsize=15)
plt.tight_layout() # Isso ajusta as margens automaticamente para nada ficar cortado
plt.savefig("Mass1Mass2.png", dpi=300) # dpi=300 deixa a imagem em alta resolução
plt.show()
shutil.move('Mass1Mass2.png', 'img_stat/Mass1Mass2.png')

mean_spin = np.mean(chi_eff)
std1_spin = np.std(chi_eff)
plt.figure(figsize=(8, 6))
plt.hist(chi_eff, bins=15, color='lightgreen', edgecolor='black')
plt.xlabel(r"Spin", fontsize=20)
plt.ylabel("Frequency", fontsize=20)
plt.title(rf'$\mu$ = {round(mean_spin,2)} $ M_\odot $,    $\sigma$ = {round(std1_spin,2)} ', fontsize=30)
plt.savefig('Spin.png', dpi=300)
shutil.move('Spin.png', 'img_stat/Spin.png')
plt.show()

'''





index_especifico = df[df['shortName'] == 'GW150914-v3'].index[0]
print(index_especifico)
print(chi_eff[index_especifico])