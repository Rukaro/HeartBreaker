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
    
    # 游戏信息
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("已击败K", f"{state['kings_defeated']}/3")
    with col2:
        st.metric("牌堆剩余", f"{state['deck_size']} 张")
    with col3:
        status = "游戏进行中" if not state['is_game_over'] else ("胜利！" if state['is_victory'] else "游戏结束")
        st.metric("状态", status)
    
    # 检查游戏是否结束
    if state['is_game_over']:
        if state['is_victory']:
            st.balloons()
            st.success("🎉 恭喜！你成功击败了所有三个K！游戏胜利！")
            if st.button("重新开始", type="primary"):
                start_new_game()
        else:
            st.error("游戏结束")
            if st.button("重新开始", type="primary"):
                start_new_game()
        return
    
    # 敌人牌区域
    st.subheader("🃏 敌人牌")
    enemy_cols = st.columns(4)
    for i, (enemy, value) in enumerate(zip(state['enemies'], enemy_values)):
        with enemy_cols[i]:
            is_king = enemy.is_king()
            card_text = card_display(enemy)
            if is_king:
                card_text += " (K)"
            
            st.write(f"**{card_text}**")
            st.write(f"点数: **{value}**")
            
            if st.button(f"攻击敌人 {i+1}", key=f"attack_enemy_{i}", disabled=st.session_state.waiting_for_discard):
                st.session_state.selected_enemy_index = i
                st.rerun()
    
    st.divider()
    
    # 手牌区域
    st.subheader("👋 你的手牌")
    hand_cols = st.columns(len(state['hand']))
    hand_values = {}
    for i, card in enumerate(state['hand']):
        with hand_cols[i]:
            numeric_value = card.get_numeric_value(game.hand)
            hand_values[i] = numeric_value
            
            is_spade_k = card.is_spade_king()
            card_text = card_display(card)
            if is_spade_k:
                card_text += " (黑桃K)"
            
            st.write(f"**{card_text}**")
            st.write(f"点数: **{numeric_value}**")
    
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
    
    st.divider()
    st.subheader(f"⚔️ 攻击敌人 {enemy_index + 1} (目标点数: {target_value})")
    
    # 选择攻击方式
    attack_mode = st.radio(
        "选择攻击方式",
        ["自动计算", "手动输入算式"],
        key="attack_mode"
    )
    
    if attack_mode == "自动计算":
        # 自动计算
        solution = game.can_defeat_enemy(enemy_index)
        
        if solution:
            expr, result = solution
            st.success("✓ 找到了解决方案！")
            st.write(f"**表达式**: `{expr}`")
            st.write(f"**计算结果**: `{result}`")
            st.write(f"**目标点数**: `{target_value}`")
            
            if st.button("确认攻击", type="primary", key="confirm_auto_attack"):
                if game.defeat_enemy(enemy_index):
                    st.success(f"✓ 成功击败敌人 {card_display(enemy)}！")
                    st.session_state.selected_enemy_index = None
                    st.session_state.waiting_for_discard = True
                    st.rerun()
                else:
                    st.error("击败敌人失败")
        else:
            st.warning("无法用当前手牌计算出该敌人的点数")
            if st.button("取消", key="cancel_auto_attack"):
                st.session_state.selected_enemy_index = None
                st.rerun()
    
    else:
        # 手动输入
        st.session_state.manual_enemy_index = enemy_index
        
        # 显示手牌点数
        st.write("**你的手牌点数：**")
        hand_points = []
        for i, card in enumerate(game.hand):
            numeric_value = card.get_numeric_value(game.hand)
            is_spade_k = card.is_spade_king()
            hand_points.append(f"{card_display(card)}: {numeric_value}" + (" (黑桃K，可用可不用)" if is_spade_k else ""))
        st.write(", ".join(hand_points))
        
        expression = st.text_input(
            "输入算式（使用 +、-、*、/ 和括号）",
            value=st.session_state.manual_expression,
            key="manual_input",
            placeholder="例如: (5 + 3) * 2"
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("验证算式", key="validate_manual"):
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
                if st.button("确认攻击", type="primary", key="confirm_manual_attack"):
                    if game.defeat_enemy(enemy_index, skip_validation=True):
                        st.success(f"✓ 成功击败敌人 {card_display(enemy)}！")
                        st.session_state.selected_enemy_index = None
                        st.session_state.manual_expression = ""
                        st.session_state.expression_valid = False
                        st.session_state.waiting_for_discard = True
                        st.rerun()
        
        with col3:
            if st.button("取消", key="cancel_manual_attack"):
                st.session_state.selected_enemy_index = None
                st.session_state.manual_expression = ""
                st.session_state.expression_valid = False
                st.rerun()

def handle_discard_selection():
    """处理丢弃手牌选择"""
    st.divider()
    st.subheader("🗑️ 选择要丢弃的手牌")
    st.write("击败敌人后，你需要丢弃一张手牌（不能丢弃黑桃K）")
    
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
    
    # 显示可丢弃的手牌
    discard_cols = st.columns(len(discardable_cards))
    for idx, (card_idx, card) in enumerate(discardable_cards):
        with discard_cols[idx]:
            card_text = card_display(card)
            numeric_value = card.get_numeric_value(game.hand)
            st.write(f"**{card_text}**")
            st.write(f"点数: {numeric_value}")
            if st.button(f"丢弃", key=f"discard_{card_idx}"):
                if game.discard_card(card_idx):
                    st.success(f"✓ 已丢弃 {card_text}")
                    st.session_state.waiting_for_discard = False
                    st.rerun()
                else:
                    st.error("无法丢弃该牌")

def main():
    """主函数"""
    # 标题
    st.title("🃏 《失心王》游戏")
    st.markdown("**黑化的国王打算杀死另外3位国王。扮演黑桃K，消灭另外三个K以获胜。**")
    
    # 侧边栏
    with st.sidebar:
        st.header("游戏规则")
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

