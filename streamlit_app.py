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
        background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 2px solid #ff6b6b;
        display: block;
        width: 100%;
        box-sizing: border-box;
    }
    
    /* 手牌区域 */
    .hand-section {
        background: linear-gradient(135deg, #f0f7ff 0%, #e5f0ff 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 2px solid #4dabf7;
        display: block;
        width: 100%;
        box-sizing: border-box;
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
    
    /* 攻击输入区域 */
    .attack-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        border: 2px solid #667eea;
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
if 'selected_enemy_index' not in st.session_state:
    st.session_state.selected_enemy_index = None
if 'waiting_for_discard' not in st.session_state:
    st.session_state.waiting_for_discard = False
if 'manual_expression' not in st.session_state:
    st.session_state.manual_expression = ""
if 'manual_enemy_index' not in st.session_state:
    st.session_state.manual_enemy_index = None
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
    st.session_state.selected_enemy_index = None
    st.session_state.waiting_for_discard = False
    st.session_state.manual_expression = ""
    st.session_state.manual_enemy_index = None
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
    
    # 敌人牌区域 - 使用完整的HTML字符串
    enemy_cards_html = []
    for i, (enemy, value) in enumerate(zip(state['enemies'], enemy_values)):
        is_king = enemy.is_king()
        card_text = card_display(enemy)
        if is_king:
            card_text += " (K)"
        
        card_class = get_card_css_class(enemy)
        card_html = f'''
        <div style="display: inline-block; margin: 10px; vertical-align: top;">
            <div class="{card_class}">
                <div class="card-value">{card_text}</div>
                <div class="card-point">点数: {value}</div>
            </div>
        </div>
        '''
        enemy_cards_html.append(card_html)
    
    enemy_section_html = f'''
    <div class="enemy-section">
        <h2 style="color: #ff6b6b; margin-bottom: 15px; padding-left: 10px; border-left: 4px solid #ff6b6b;">🃏 敌人牌</h2>
        <div style="text-align: center; margin-bottom: 15px;">
            {''.join(enemy_cards_html)}
        </div>
    </div>
    '''
    st.markdown(enemy_section_html, unsafe_allow_html=True)
    
    # 按钮区域 - 放在div外面
    enemy_cols = st.columns(4)
    for i, (enemy, value) in enumerate(zip(state['enemies'], enemy_values)):
        with enemy_cols[i]:
            if st.button("攻击敌人", key=f"attack_enemy_{i}", disabled=st.session_state.waiting_for_discard, use_container_width=True):
                st.session_state.selected_enemy_index = i
                st.rerun()
    
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
        card_html = f'''
        <div style="display: inline-block; margin: 10px; vertical-align: top;">
            <div class="{card_class}">
                <div class="card-value">{card_text}</div>
                <div class="card-point">点数: {numeric_value}</div>
            </div>
        </div>
        '''
        hand_cards_html.append(card_html)
    
    hand_section_html = f'''
    <div class="hand-section">
        <h2 style="color: #4dabf7; margin-bottom: 15px; padding-left: 10px; border-left: 4px solid #4dabf7;">👋 你的手牌</h2>
        <div style="text-align: center;">
            {''.join(hand_cards_html)}
        </div>
    </div>
    '''
    st.markdown(hand_section_html, unsafe_allow_html=True)
    
    # 处理攻击选择
    if st.session_state.selected_enemy_index is not None:
        handle_attack_selection()
    
    # 处理丢弃手牌
    if st.session_state.waiting_for_discard:
        handle_discard_selection()

def handle_attack_selection():
    """处理攻击选择"""
    enemy_index = st.session_state.selected_enemy_index
    game = st.session_state.game
    
    if enemy_index < 0 or enemy_index >= len(game.enemies):
        st.error("无效的敌人索引")
        st.session_state.selected_enemy_index = None
        return
    
    enemy = game.enemies[enemy_index]
    target_value = enemy.get_numeric_value(game.enemies)
    
    st.markdown('<div class="attack-section">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color: #667eea; margin-bottom: 15px;">⚔️ 攻击敌人 {enemy_index + 1} (目标点数: {target_value})</h3>', unsafe_allow_html=True)
    
    # 显示手牌点数
    st.markdown('<div class="hand-values-hint">', unsafe_allow_html=True)
    st.markdown("**你的手牌点数：**")
    hand_points = []
    for i, card in enumerate(game.hand):
        numeric_value = card.get_numeric_value(game.hand)
        is_spade_k = card.is_spade_king()
        hand_points.append(f"{card_display(card)}: {numeric_value}" + (" (黑桃K，可用可不用)" if is_spade_k else ""))
    st.markdown(", ".join(hand_points))
    st.markdown('</div>', unsafe_allow_html=True)
    
    expression = st.text_input(
        "输入算式（使用 +、-、*、/ 和括号）",
        value=st.session_state.manual_expression,
        key="manual_input",
        placeholder="例如: (5 + 3) * 2"
    )
    st.markdown('<p style="font-size: 0.9em; color: #666; margin-top: 5px; font-style: italic;">示例: (11 + 5) * 2, 13 - 5 + 3, (12 + 4) / 2</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("验证算式", key="validate_manual", use_container_width=True):
            if expression:
                # 验证算式
                try:
                    result = eval(expression)
                    if abs(result - target_value) > 0.0001:
                        st.error(f"计算结果 {result} 不等于目标点数 {target_value}")
                        st.session_state.expression_valid = False
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
                            st.session_state.expression_valid = False
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
                                st.session_state.expression_valid = False
                            else:
                                st.success("✓ 算式有效！")
                                st.session_state.manual_expression = expression
                                st.session_state.expression_valid = True
                except Exception as e:
                    st.error(f"算式无效: {str(e)}")
                    st.session_state.expression_valid = False
            else:
                st.warning("请输入算式")
    
    with col2:
        if st.session_state.expression_valid:
            if st.button("确认攻击", type="primary", key="confirm_manual_attack", use_container_width=True):
                if game.defeat_enemy(enemy_index, skip_validation=True):
                    st.success(f"✓ 成功击败敌人 {card_display(enemy)}！")
                    st.session_state.selected_enemy_index = None
                    st.session_state.manual_expression = ""
                    st.session_state.expression_valid = False
                    st.session_state.waiting_for_discard = True
                    st.rerun()
    
    with col3:
        if st.button("取消", key="cancel_manual_attack", use_container_width=True):
            st.session_state.selected_enemy_index = None
            st.session_state.manual_expression = ""
            st.session_state.expression_valid = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def handle_discard_selection():
    """处理丢弃手牌选择"""
    game = st.session_state.game
    state = game.get_game_state()
    
    # 获取可丢弃的手牌（不包括黑桃K）
    discardable_cards = []
    for i, card in enumerate(state['hand']):
        if not card.is_spade_king():
            discardable_cards.append((i, card))
    
    if len(discardable_cards) == 0:
        st.error("没有可丢弃的手牌（除了黑桃K）")
        st.session_state.waiting_for_discard = False
        return
    
    # 创建可丢弃的手牌HTML
    discard_cards_html = []
    for idx, (card_idx, card) in enumerate(discardable_cards):
        card_text = card_display(card)
        numeric_value = card.get_numeric_value(game.hand)
        card_class = get_card_css_class(card)
        card_html = f'''
        <div style="display: inline-block; margin: 10px; vertical-align: top;">
            <div class="{card_class}">
                <div class="card-value">{card_text}</div>
                <div class="card-point">点数: {numeric_value}</div>
            </div>
        </div>
        '''
        discard_cards_html.append(card_html)
    
    # 使用完整的HTML字符串
    discard_section_html = f'''
    <div class="discard-section">
        <h3 style="color: #ffd43b; margin-bottom: 15px;">🗑️ 选择要丢弃的手牌</h3>
        <p style="color: #666; margin-bottom: 15px; font-style: italic;">击败敌人后，你需要丢弃一张手牌（不能丢弃黑桃K）</p>
        <div style="text-align: center; margin-bottom: 15px;">
            {''.join(discard_cards_html)}
        </div>
    </div>
    '''
    st.markdown(discard_section_html, unsafe_allow_html=True)
    
    # 按钮区域 - 放在div外面
    discard_cols = st.columns(len(discardable_cards) + 1)  # +1 for cancel button
    for idx, (card_idx, card) in enumerate(discardable_cards):
        with discard_cols[idx]:
            if st.button(f"丢弃", key=f"discard_{card_idx}", use_container_width=True):
                if game.discard_card(card_idx):
                    st.success(f"✓ 已丢弃 {card_display(card)}")
                    st.session_state.waiting_for_discard = False
                    st.rerun()
                else:
                    st.error("无法丢弃该牌")
    
    with discard_cols[len(discardable_cards)]:
        if st.button("取消", key="cancel_discard", use_container_width=True):
            st.session_state.waiting_for_discard = False
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
