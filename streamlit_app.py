"""
失心王游戏 - Streamlit版本
"""
import streamlit as st
from game import Game
from card import Card, Suit

# 页面配置
st.set_page_config(
    page_title="失心王游戏",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式，参考Flask版本
st.markdown("""
<style>
    /* 主容器样式 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* 标题样式 */
    h1 {
        font-size: 2.5em !important;
        color: #667eea !important;
        text-align: center;
        margin-bottom: 10px !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* 副标题样式 */
    .subtitle {
        font-size: 1.1em;
        color: #666;
        text-align: center;
        margin-bottom: 30px;
        line-height: 1.6;
    }
    
    /* 游戏信息卡片 */
    .game-info {
        background: linear-gradient(135deg, #f5f5f5 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        border: 2px solid #667eea;
    }
    
    /* 敌人牌区域 */
    .enemy-section {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%) !important;
        padding: 20px !important;
        border-radius: 10px !important;
        margin-bottom: 20px !important;
        border: 2px solid #ff6b6b !important;
        display: block !important;
        width: 100% !important;
        box-sizing: border-box !important;
        overflow: visible !important;
    }
    
    /* 手牌区域 */
    .hand-section {
        background: linear-gradient(135deg, #f0f7ff 0%, #e5f0ff 100%) !important;
        padding: 20px !important;
        border-radius: 10px !important;
        margin-bottom: 20px !important;
        border: 2px solid #4dabf7 !important;
        display: block !important;
        width: 100% !important;
        box-sizing: border-box !important;
        overflow: visible !important;
    }
    
    /* 卡片容器区域 */
    .cards-container {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        align-items: flex-start !important;
        gap: 15px !important;
        width: 100% !important;
    }
    
    /* 卡片样式 - 固定比例，像真实卡牌 */
    .card-container {
        width: 100px;
        height: 140px;
        aspect-ratio: 5 / 7;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        text-align: center;
        transition: all 0.3s ease;
        border: 3px solid;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        position: relative;
    }
    
    .card-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* 根据花色设置颜色 */
    .card-spade {
        background: linear-gradient(135deg, #2c3e50 0%, #1a252f 100%);
        color: white;
        border-color: #0d1117 !important;
    }
    
    .card-heart {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        border-color: #a93226 !important;
    }
    
    .card-diamond {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        border-color: #a93226 !important;
    }
    
    .card-club {
        background: linear-gradient(135deg, #2c3e50 0%, #1a252f 100%);
        color: white;
        border-color: #0d1117 !important;
    }
    
    .card-joker {
        background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        color: #fff;
        border-color: #d35400 !important;
    }
    
    /* 黑桃K特殊样式 */
    .card-spade-king {
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
        color: #ffd700;
        border-color: #ffd700 !important;
        border-width: 4px !important;
    }
    
    /* 卡片文字 */
    .card-value {
        font-size: 1.8em;
        font-weight: bold;
        margin-bottom: 5px;
        line-height: 1.2;
    }
    
    .card-point {
        font-size: 0.9em;
        opacity: 0.9;
        margin-top: 5px;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* 战斗区 */
    .battle-section {
        background: linear-gradient(135deg, #fff9e6 0%, #ffe5cc 100%);
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        border: 3px solid #ff6b6b;
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-height: 200px;
    }
    
    /* 战斗区左侧 */
    .battle-left {
        flex: 1;
        padding-right: 20px;
    }
    
    /* 战斗区中间 */
    .battle-center {
        flex: 0 0 auto;
        padding: 0 20px;
    }
    
    /* 战斗区右侧 */
    .battle-right {
        flex: 1;
        padding-left: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* 可点击的敌人牌 */
    .enemy-card-clickable {
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .enemy-card-clickable:hover {
        transform: scale(1.1);
        box-shadow: 0 8px 16px rgba(255, 107, 107, 0.4);
    }
    
    /* 手牌点数提示 */
    .hand-values-hint {
        background: #e9ecef;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input {
        border: 2px solid #667eea;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #764ba2;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* 丢弃手牌区域 */
    .discard-section {
        background: linear-gradient(135deg, #fff9e6 0%, #ffe5cc 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border: 2px solid #ffd43b;
    }
    
    /* 成功消息 */
    .stSuccess {
        background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        border: none;
    }
    
    /* 错误消息 */
    .stError {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        border: none;
    }
    
    /* 警告消息 */
    .stWarning {
        background: linear-gradient(135deg, #ffd43b 0%, #ffc107 100%);
        color: #333;
        padding: 15px;
        border-radius: 8px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'game' not in st.session_state:
    st.session_state.game = None
if 'battle_enemy_index' not in st.session_state:
    st.session_state.battle_enemy_index = None  # 战斗区选中的敌人索引
if 'waiting_for_discard' not in st.session_state:
    st.session_state.waiting_for_discard = False
if 'manual_expression' not in st.session_state:
    st.session_state.manual_expression = ""
if 'expression_valid' not in st.session_state:
    st.session_state.expression_valid = False

def card_display(card: Card, is_enemy: bool = False) -> str:
    """格式化显示卡片"""
    if card.suit == Suit.JOKER:
        return "大王" if card.is_big_joker else "小王"
    else:
        value_str = card.get_value_str()
        return f"{card.suit.value}{value_str}"

def get_card_css_class(card: Card) -> str:
    """根据花色返回卡片的CSS类名"""
    if card.is_spade_king():
        return "card-container card-spade-king"
    elif card.suit == Suit.SPADE:
        return "card-container card-spade"
    elif card.suit == Suit.HEART:
        return "card-container card-heart"
    elif card.suit == Suit.DIAMOND:
        return "card-container card-diamond"
    elif card.suit == Suit.CLUB:
        return "card-container card-club"
    elif card.suit == Suit.JOKER:
        return "card-container card-joker"
    else:
        return "card-container"

def start_new_game():
    """开始新游戏"""
    st.session_state.game = Game()
    st.session_state.battle_enemy_index = None
    st.session_state.waiting_for_discard = False
    st.session_state.manual_expression = ""
    st.session_state.expression_valid = False
    st.rerun()

def display_game_state():
    """显示游戏状态"""
    if st.session_state.game is None:
        st.warning("请先开始新游戏")
        return
    
    game = st.session_state.game
    state = game.get_game_state()
    enemy_values = game.get_enemy_values()
    
    # 游戏信息卡片 - 使用完整的HTML字符串
    status = "游戏进行中" if not state['is_game_over'] else ("胜利！" if state['is_victory'] else "游戏结束")
    status_color = "#51cf66" if state['is_victory'] else "#667eea" if not state['is_game_over'] else "#ff6b6b"
    game_info_html = f'''
    <div class="game-info">
        <div style="display: flex; justify-content: space-around; align-items: center;">
            <div style="text-align: center;">
                <h3 style="color: #667eea; margin: 0;">已击败K</h3>
                <p style="font-size: 1.5em; font-weight: bold; color: #667eea; margin: 5px 0;">{state["kings_defeated"]}/3</p>
            </div>
            <div style="text-align: center;">
                <h3 style="color: #667eea; margin: 0;">牌堆剩余</h3>
                <p style="font-size: 1.5em; font-weight: bold; color: #667eea; margin: 5px 0;">{state["deck_size"]} 张</p>
            </div>
            <div style="text-align: center;">
                <h3 style="color: #667eea; margin: 0;">状态</h3>
                <p style="font-size: 1.5em; font-weight: bold; color: {status_color}; margin: 5px 0;">{status}</p>
            </div>
        </div>
    </div>
    '''
    st.markdown(game_info_html, unsafe_allow_html=True)
    
    # 检查游戏是否结束
    if state['is_game_over']:
        if state['is_victory']:
            st.balloons()
            st.success("🎉 恭喜！你成功击败了所有三个K！游戏胜利！")
            if st.button("重新开始", type="primary", use_container_width=True):
                start_new_game()
        else:
            st.error("游戏结束")
            if st.button("重新开始", type="primary", use_container_width=True):
                start_new_game()
        return
    
    # 敌人牌区域 - 标题和卡片
    enemy_section_html = f'<div class="enemy-section"><h2 style="color: #ff6b6b; margin-bottom: 15px; padding-left: 10px; border-left: 4px solid #ff6b6b;">🃏 敌人牌（点击卡片下方按钮选择）</h2></div>'
    st.markdown(enemy_section_html, unsafe_allow_html=True)
    
    # 敌人牌卡片和按钮
    enemy_cols = st.columns(4)
    for i, (enemy, value) in enumerate(zip(state['enemies'], enemy_values)):
        is_king = enemy.is_king()
        card_text = card_display(enemy)
        if is_king:
            card_text += " (K)"
        
        card_class = get_card_css_class(enemy)
        # 如果这个敌人已经在战斗区，添加选中样式
        selected_style = "border: 4px solid #51cf66 !important; box-shadow: 0 0 15px rgba(81, 207, 102, 0.5) !important;" if st.session_state.battle_enemy_index == i else ""
        card_html = f'<div class="{card_class}" style="{selected_style}"><div class="card-value">{card_text}</div><div class="card-point">点数: {value}</div></div>'
        
        # 在每个列中显示卡片和按钮
        with enemy_cols[i]:
            st.markdown(card_html, unsafe_allow_html=True)
            # 点击按钮选择敌人
            button_text = "取消选择" if st.session_state.battle_enemy_index == i else "选择"
            if st.button(button_text, key=f"select_enemy_{i}", disabled=st.session_state.waiting_for_discard, use_container_width=True):
                if st.session_state.battle_enemy_index == i:
                    st.session_state.battle_enemy_index = None
                else:
                    st.session_state.battle_enemy_index = i
                    st.session_state.manual_expression = ""
                    st.session_state.expression_valid = False
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 战斗区 - 始终显示
    display_battle_area()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 手牌区域 - 使用完整的HTML字符串
    hand_cards_html = []
    for i, card in enumerate(state['hand']):
        numeric_value = card.get_numeric_value(game.hand)
        is_spade_k = card.is_spade_king()
        card_text = card_display(card)
        
        if is_spade_k:
            card_text += " (黑桃K)"
        
        card_class = get_card_css_class(card)
        card_html = f'<div class="{card_class}"><div class="card-value">{card_text}</div><div class="card-point">点数: {numeric_value}</div></div>'
        hand_cards_html.append(card_html)
    
    hand_section_html = f'<div class="hand-section"><h2 style="color: #4dabf7; margin-bottom: 15px; padding-left: 10px; border-left: 4px solid #4dabf7;">👋 你的手牌</h2><div class="cards-container">{"".join(hand_cards_html)}</div></div>'
    st.markdown(hand_section_html, unsafe_allow_html=True)
    
    # 处理丢弃手牌 - 在手牌下方显示丢弃按钮
    if st.session_state.waiting_for_discard:
        st.warning("请选择要丢弃的手牌（不能丢弃黑桃K）")
        discard_cols = st.columns(len(state['hand']))
        for i, card in enumerate(state['hand']):
            with discard_cols[i]:
                is_spade_k = card.is_spade_king()
                card_text = card_display(card)
                if not is_spade_k:
                    if st.button(f"丢弃 {card_text}", key=f"discard_{i}", use_container_width=True):
                        if game.discard_card(i):
                            st.success(f"✓ 已丢弃 {card_text}")
                            st.session_state.waiting_for_discard = False
                            st.rerun()
                        else:
                            st.error("无法丢弃该牌")
                else:
                    st.write("(黑桃K，不可丢弃)")

def display_battle_area():
    """显示战斗区（始终显示）"""
    game = st.session_state.game
    battle_enemy_index = st.session_state.battle_enemy_index
    
    # 显示手牌点数提示
    hand_points = []
    for i, card in enumerate(game.hand):
        numeric_value = card.get_numeric_value(game.hand)
        is_spade_k = card.is_spade_king()
        hand_points.append(f"{card_display(card)}: {numeric_value}" + (" (黑桃K，可用可不用)" if is_spade_k else ""))
    hand_points_text = ", ".join(hand_points)
    
    # 如果有选中的敌人
    if battle_enemy_index is not None and battle_enemy_index >= 0 and battle_enemy_index < len(game.enemies):
        enemy = game.enemies[battle_enemy_index]
        target_value = enemy.get_numeric_value(game.enemies)
        
        # 战斗区HTML - 右侧显示敌人
        is_king = enemy.is_king()
        card_text = card_display(enemy)
        if is_king:
            card_text += " (K)"
        card_class = get_card_css_class(enemy)
        enemy_card_html = f'<div class="{card_class}"><div class="card-value">{card_text}</div><div class="card-point">点数: {target_value}</div></div>'
        
        battle_left_content = f'<h3 style="color: #667eea; margin-bottom: 10px;">⚔️ 战斗区</h3><p style="font-size: 0.9em; color: #666; margin-bottom: 10px;"><strong>目标点数:</strong> {target_value}</p><p style="font-size: 0.85em; color: #666; margin-bottom: 15px;"><strong>手牌点数:</strong> {hand_points_text}</p>'
        battle_right_content = enemy_card_html
    else:
        # 没有选中敌人
        battle_left_content = f'<h3 style="color: #667eea; margin-bottom: 10px;">⚔️ 战斗区</h3><p style="font-size: 0.9em; color: #666; margin-bottom: 10px;"><strong>目标点数:</strong> 请先选择敌人</p><p style="font-size: 0.85em; color: #666; margin-bottom: 15px;"><strong>手牌点数:</strong> {hand_points_text}</p>'
        battle_right_content = '<div style="text-align: center; color: #999; padding: 20px;">请选择敌人</div>'
    
    # 战斗区完整HTML - 使用完整字符串
    battle_section_html = f'<div class="battle-section"><div class="battle-left">{battle_left_content}</div><div class="battle-center"></div><div class="battle-right">{battle_right_content}</div></div>'
    st.markdown(battle_section_html, unsafe_allow_html=True)
    
    # 算式输入和攻击按钮 - 放在div外面
    battle_col1, battle_col2, battle_col3 = st.columns([2, 1, 1])
    
    with battle_col1:
        expression = st.text_input(
            "输入算式（使用 +、-、*、/ 和括号）",
            value=st.session_state.manual_expression,
            key="battle_expression",
            placeholder="例如: (5 + 3) * 2",
            disabled=battle_enemy_index is None
        )
        st.markdown('<p style="font-size: 0.85em; color: #666; margin-top: 5px; font-style: italic;">示例: (11 + 5) * 2, 13 - 5 + 3</p>', unsafe_allow_html=True)
    
    with battle_col2:
        if st.button("⚔️\n攻\n击", type="primary", key="battle_attack", use_container_width=True, disabled=st.session_state.waiting_for_discard or battle_enemy_index is None):
            if battle_enemy_index is None:
                st.warning("请先选择敌人")
            elif expression:
                # 验证并攻击
                try:
                    result = eval(expression)
                    enemy = game.enemies[battle_enemy_index]
                    target_value = enemy.get_numeric_value(game.enemies)
                    if abs(result - target_value) > 0.0001:
                        st.error(f"计算结果 {result} 不等于目标点数 {target_value}")
                    else:
                        # 验证使用的牌
                        import re
                        numbers_in_expr = re.findall(r'\d+\.?\d*', expression)
                        used_values = [float(n) for n in numbers_in_expr]
                        
                        # 获取必须使用的牌（除黑桃K外的所有牌）
                        required_cards = [c for c in game.hand if not c.is_spade_king()]
                        required_values = [c.get_numeric_value(game.hand) for c in required_cards]
                        
                        # 检查是否所有必须的牌都被使用
                        used_values_copy = used_values.copy()
                        missing_cards = []
                        for req_val in required_values:
                            found = False
                            for i, used_val in enumerate(used_values_copy):
                                if abs(used_val - req_val) < 0.0001:
                                    used_values_copy.pop(i)
                                    found = True
                                    break
                            if not found:
                                missing_cards.append(req_val)
                        
                        if missing_cards:
                            st.error(f"未使用所有必须的手牌（缺少点数: {missing_cards}）")
                        else:
                            # 检查使用的数字是否都在手牌中
                            invalid_values = []
                            for used_val in used_values:
                                valid = False
                                for card in game.hand:
                                    card_val = card.get_numeric_value(game.hand)
                                    if abs(card_val - used_val) < 0.0001:
                                        valid = True
                                        break
                                if not valid:
                                    invalid_values.append(used_val)
                            
                            if invalid_values:
                                st.error(f"使用了不在手牌中的点数: {invalid_values}")
                            else:
                                # 攻击成功
                                enemy = game.enemies[battle_enemy_index]
                                card_text = card_display(enemy)
                                if game.defeat_enemy(battle_enemy_index, skip_validation=True):
                                    st.success(f"✓ 成功击败敌人 {card_text}！")
                                    st.session_state.battle_enemy_index = None
                                    st.session_state.manual_expression = ""
                                    st.session_state.expression_valid = False
                                    st.session_state.waiting_for_discard = True
                                    st.rerun()
                                else:
                                    st.error("攻击失败")
                except Exception as e:
                    st.error(f"算式无效: {str(e)}")
            else:
                st.warning("请输入算式")
    
    with battle_col3:
        if battle_enemy_index is not None:
            if st.button("取消", key="cancel_battle", use_container_width=True):
                st.session_state.battle_enemy_index = None
                st.session_state.manual_expression = ""
                st.session_state.expression_valid = False
                st.rerun()


def main():
    """主函数"""
    # 标题
    st.markdown('<h1>《失心王》</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">黑化的国王打算杀死另外3位国王。扮演黑桃K，消灭另外三个K以获胜。</p>', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.header("📖 游戏规则")
        st.markdown("""
        1. **游戏开始**：玩家拥有黑桃K和另外4张随机牌（共5张手牌）
        2. **敌人**：翻开牌堆顶的4张牌作为敌人
        3. **攻击规则**：
           - 玩家需用手上的牌结合四则运算计算出对面的其中一个点数
           - J、Q、K视为11、12、13
           - 大王的点数始终视为另外三张牌里最大的一个
           - 小王视为最小
           - **除黑桃K之外的牌必须全部用到，黑桃K可用可不用**
        4. **战斗流程**：
           - 每战胜一个敌人，玩家需要：
             - 抛弃4张手牌之一（不能丢弃黑桃K）
             - 将刚刚消灭的敌人加入手牌
             - 翻开新的牌直到有4个敌人
        5. **胜利条件**：消灭其余3个K（红心K、方块K、梅花K）即为胜利
        """)
        
        st.divider()
        
        if st.button("🔄 新游戏", type="primary", use_container_width=True):
            start_new_game()
        
        if st.button("🔄 刷新状态", use_container_width=True):
            st.rerun()
    
    # 主内容
    if st.session_state.game is None:
        st.info("👈 点击侧边栏的「新游戏」按钮开始游戏")
    else:
        display_game_state()

if __name__ == "__main__":
    main()
