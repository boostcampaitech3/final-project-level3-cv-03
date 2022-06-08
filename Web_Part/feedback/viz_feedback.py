#%% Import library
import numpy as np
import pandas as pd
import matplotlib as mpl
import os
import seaborn as sns

from matplotlib import pyplot as plt
from matplotlib import font_manager, rc

#%% Custom functions
def save_fig(path:str=None, dpi:int=150):
    plt.savefig(path+'.png', dpi=dpi)
    plt.close()

#%% Set matplotlib style
# Set total style
plt.style.use('default')

# Korean font
font_files = font_manager.findSystemFonts(fontpaths='./fonts')

for font_file in font_files:
    font_manager.fontManager.addfont(font_file)

kfont_path = "./fonts/NanumBarunGothic.ttf"
kfont_nm = font_manager.FontProperties(fname=kfont_path).get_name()
rc('font', family=kfont_nm)

# Font size
SMALL_SIZE=10
MEDIUM_SIZE=15
LARGE_SIZE=20

plt.rc('font', size=MEDIUM_SIZE, weight='bold')
plt.rc('xtick', labelsize=LARGE_SIZE)
plt.rc('ytick', labelsize=LARGE_SIZE)
plt.rc('axes', labelsize=LARGE_SIZE, labelweight='bold')
plt.rc('legend', fontsize=LARGE_SIZE)

#%% Make figure save directory
fig_dir_nm = 'figures_feedback_analysis/'
if not os.path.isdir(fig_dir_nm):
    os.mkdir(fig_dir_nm)

#%% Load feedback files and preprocess
# Load feedback file
df_feedback_raw = pd.read_csv('배우고 싶니_ 서비스 피드백 설문지(응답) - 설문지 응답 시트1.csv')

# Remove unnecessary rows
df_feedback = df_feedback_raw[~df_feedback_raw['타임스탬프'].isnull()]

#%% Analyze feedback by coding experiences
df_by_coding = df_feedback.groupby(by='개발 경험이 있으신가요?')

num_code_positive, num_code_negative = \
    df_feedback['개발 경험이 있으신가요?'].value_counts()['네'],\
    df_feedback['개발 경험이 있으신가요?'].value_counts()['아니오']

# plot - Numerical feature average by coding experiences
fig_mean_by_code, ax_mean_by_code = plt.subplots(1, 1, figsize=(12, 8))

ax_mean_by_code.spines['top'].set_linewidth(0)
ax_mean_by_code.spines['right'].set_linewidth(0)

ax_mean_by_code.barh(
    np.array([1, 2, 3])-0.15, df_by_coding.mean().loc['네', :],
    0.25,  
    label=f'코딩경험 있음 (N={num_code_positive})'
    )
ax_mean_by_code.barh(
    np.array([1, 2, 3])+0.15, df_by_coding.mean().loc['아니오', :], 
    0.25, 
    label=f'코딩경험 없음 (N={num_code_negative})'
    )
ax_mean_by_code.invert_yaxis()

ax_mean_by_code.set_yticks([1, 2, 3])
ax_mean_by_code.set_yticklabels(['서비스 만족도', '서비스 체감 속도', '배우가 닮게 느껴지는 정도'])
ax_mean_by_code.set_xlabel('사용자 긍정 평가 (0 최하, 5 최상)')
ax_mean_by_code.legend()
fig_mean_by_code.tight_layout()

save_fig(os.path.join(fig_dir_nm, '수치형 자료 평균 비교 (코딩 경험 유무 기준)'))


# plot - Numerical feature average by coding experiences
fig_median_by_code, ax_median_by_code = plt.subplots(1, 1, figsize=(12, 8))

ax_median_by_code.spines['top'].set_linewidth(0)
ax_median_by_code.spines['right'].set_linewidth(0)

ax_median_by_code.barh(
    np.array([1, 2, 3])-0.15, df_by_coding.median().loc['네', :],
    0.25,  
    label=f'코딩경험 있음 (N={num_code_positive})'
    )
ax_median_by_code.barh(
    np.array([1, 2, 3])+0.15, df_by_coding.median().loc['아니오', :], 
    0.25, 
    label=f'코딩경험 없음 (N={num_code_negative})'
    )
ax_median_by_code.invert_yaxis()

ax_median_by_code.set_yticks([1, 2, 3])
ax_median_by_code.set_yticklabels(['서비스 만족도', '서비스 체감 속도', '배우가 닮게 느껴지는 정도'])
ax_median_by_code.set_xlabel('사용자 긍정 평가 (0 최하, 5 최상)')
ax_median_by_code.legend()
fig_median_by_code.tight_layout()

save_fig(os.path.join(fig_dir_nm, '수치형 자료 중앙값 비교 (코딩 경험 유무 기준)'))

#%% Analyze feedback by gender
df_by_gender = df_feedback.groupby(by='1.  본인의 성별')

num_female, num_male = \
    df_feedback['1.  본인의 성별'].value_counts()['여성'],\
    df_feedback['1.  본인의 성별'].value_counts()['남성']

# plot - Numerical feature average by gender
fig_mean_by_gender, ax_mean_by_gender = plt.subplots(1, 1, figsize=(12, 8))

ax_mean_by_gender.spines['top'].set_linewidth(0)
ax_mean_by_gender.spines['right'].set_linewidth(0)

ax_mean_by_gender.barh(
    np.array([1, 2, 3])-0.15, df_by_gender.mean().loc['여성', :],
    0.25,  
    label=f'여성 (N={num_female})'
    )
ax_mean_by_gender.barh(
    np.array([1, 2, 3])+0.15, df_by_gender.mean().loc['남성', :], 
    0.25, 
    label=f'남성 (N={num_male})'
    )
ax_mean_by_gender.invert_yaxis()

ax_mean_by_gender.set_yticks([1, 2, 3])
ax_mean_by_gender.set_yticklabels(['서비스 만족도', '서비스 체감 속도', '배우가 닮게 느껴지는 정도'])
ax_mean_by_gender.set_xlabel('사용자 긍정 평가 (0 최하, 5 최상)')
ax_mean_by_gender.legend()
fig_mean_by_gender.tight_layout()

save_fig(os.path.join(fig_dir_nm, '수치형 자료 평균 비교 (성별 기준)'))

# plot - Numerical feature median by gender
fig_median_by_gender, ax_median_by_gender = plt.subplots(1, 1, figsize=(12, 8))

ax_median_by_gender.spines['top'].set_linewidth(0)
ax_median_by_gender.spines['right'].set_linewidth(0)

ax_median_by_gender.barh(
    np.array([1, 2, 3])-0.15, df_by_gender.median().loc['여성', :],
    0.25,  
    label=f'여성 (N={num_female})'
    )
ax_median_by_gender.barh(
    np.array([1, 2, 3])+0.15, df_by_gender.median().loc['남성', :], 
    0.25, 
    label=f'남성 (N={num_male})'
    )
ax_median_by_gender.invert_yaxis()

ax_median_by_gender.set_yticks([1, 2, 3])
ax_median_by_gender.set_yticklabels(['서비스 만족도', '서비스 체감 속도', '배우가 닮게 느껴지는 정도'])
ax_median_by_gender.set_xlabel('사용자 긍정 평가 (0 최하, 5 최상)')
ax_median_by_gender.legend()
fig_median_by_gender.tight_layout()

save_fig(os.path.join(fig_dir_nm, '수치형 자료 중앙값 비교 (성별 기준)'))

#%% Analysis by both gender and coding experience
# plot - satisfaction bar chart by gender and coding experience
fig_mean_by_two_factor = sns.catplot(
    x='3. 전반적인 만족도', 
    y='1.  본인의 성별',
    hue='개발 경험이 있으신가요?',
    data=df_feedback,
    kind='bar',
    height=6,
    aspect=1.5,
    ci='sd',
    )
fig_mean_by_two_factor.ax.set_ylabel('성별')
fig_mean_by_two_factor.ax.set_xlabel('사용자 긍정 평가 (1: 최하, 5: 최상)')
fig_mean_by_two_factor.ax.set_xlim([0, 5])

save_fig(os.path.join(fig_dir_nm, 'seaborn test'))