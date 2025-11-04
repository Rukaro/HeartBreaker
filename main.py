"""
失心王游戏主程序
"""
from game import Game
from card import Card


def display_game(game: Game):
    """显示游戏状态"""
    state = game.get_game_state()
    
    print("\n" + "=" * 60)
    print("《失心王》游戏")
    print("=" * 60)
    
    # 显示手牌
    print("\n【你的手牌】")
    for i, card in enumerate(state['hand']):
        marker = " (黑桃K)" if card.is_spade_king() else ""
        print(f"  {i + 1}. {card}{marker}")
    
    # 显示敌人
    print("\n【敌人牌】")
    enemy_values = game.get_enemy_values()
    for i, (enemy, value) in enumerate(zip(state['enemies'], enemy_values)):
        marker = " (K)" if enemy.is_king() else ""
        print(f"  {i + 1}. {enemy} (点数: {value}){marker}")
    
    # 显示游戏进度
    print(f"\n【游戏进度】已击败K: {state['kings_defeated']}/3")
    print(f"【牌堆剩余】{state['deck_size']} 张")


def display_solution(solution: tuple, enemy_value: int):
    """显示解决方案"""
    expr, result = solution
    print(f"\n✓ 找到了解决方案！")
    print(f"  目标点数: {enemy_value}")
    print(f"  计算结果: {result}")
    print(f"  表达式: {expr}")


def get_user_choice(prompt: str, valid_choices: list) -> int:
    """获取用户选择"""
    while True:
        try:
            choice = input(prompt)
            choice = int(choice)
            if choice in valid_choices:
                return choice
            else:
                print(f"无效选择，请输入 {valid_choices} 中的一个")
        except ValueError:
            print("请输入有效的数字")
        except KeyboardInterrupt:
            print("\n\n游戏已退出")
            exit(0)


def main():
    """主函数"""
    print("欢迎来到《失心王》游戏！")
    print("你的目标是扮演黑桃K，消灭另外三个K以获胜。")
    print("使用手牌通过四则运算计算出敌人的点数即可击败敌人。")
    print("除黑桃K之外的牌必须全部用到，黑桃K可用可不用。")
    print("\n按 Ctrl+C 退出游戏\n")
    
    game = Game()
    
    while not game.is_game_over:
        # 显示游戏状态
        display_game(game)
        
        # 检查是否还有敌人
        if len(game.enemies) == 0 and len(game.deck) == 0:
            print("\n游戏结束：没有更多敌人了")
            break
        
        # 让玩家选择要攻击的敌人
        print("\n【选择操作】")
        print("请选择要攻击的敌人（输入数字）:")
        
        enemy_indices = list(range(len(game.enemies)))
        enemy_choice = get_user_choice("请输入敌人编号: ", [i + 1 for i in enemy_indices])
        enemy_index = enemy_choice - 1
        
        # 检查是否能击败这个敌人
        solution = game.can_defeat_enemy(enemy_index)
        
        if solution:
            # 显示解决方案
            enemy = game.enemies[enemy_index]
            enemy_value = enemy.get_numeric_value(game.enemies)
            display_solution(solution, enemy_value)
            
            # 确认攻击
            confirm = input("\n确认攻击这个敌人？(y/n): ").strip().lower()
            if confirm == 'y':
                # 击败敌人
                if game.defeat_enemy(enemy_index):
                    print(f"\n✓ 成功击败敌人 {enemy}！")
                    
                    # 检查胜利
                    if game.is_victory:
                        print("\n" + "=" * 60)
                        print("🎉 恭喜！你成功击败了所有三个K！")
                        print("游戏胜利！")
                        print("=" * 60)
                        break
                    
                    # 需要丢弃一张手牌
                    print("\n【丢弃手牌】")
                    print("击败敌人后，你需要丢弃一张手牌（不能丢弃黑桃K）")
                    display_game(game)
                    
                    # 获取可丢弃的手牌（不包括黑桃K）
                    discardable_indices = []
                    for i, card in enumerate(game.hand):
                        if not card.is_spade_king():
                            discardable_indices.append(i + 1)
                    
                    if len(discardable_indices) > 0:
                        print("\n可丢弃的手牌:")
                        for i, card in enumerate(game.hand):
                            if not card.is_spade_king():
                                print(f"  {i + 1}. {card}")
                        
                        discard_choice = get_user_choice(
                            "请选择要丢弃的手牌编号: ",
                            discardable_indices
                        )
                        discard_index = discard_choice - 1
                        
                        # 调整索引（因为手牌列表可能已经变化）
                        # 重新找到要丢弃的牌
                        non_spade_k_cards = [(i, c) for i, c in enumerate(game.hand) if not c.is_spade_king()]
                        if discard_choice <= len(non_spade_k_cards):
                            actual_index = non_spade_k_cards[discard_choice - 1][0]
                            discarded = game.hand[actual_index]
                            game.discard_card(actual_index)
                            print(f"\n✓ 已丢弃 {discarded}")
                        else:
                            print("\n错误：无法丢弃该牌")
                    else:
                        print("\n警告：没有可丢弃的手牌（除了黑桃K）")
                else:
                    print("\n✗ 击败敌人失败")
            else:
                print("\n已取消攻击")
        else:
            print(f"\n✗ 无法用当前手牌计算出敌人 {game.enemies[enemy_index]} 的点数")
            print("请尝试攻击其他敌人")
    
    # 游戏结束
    if not game.is_victory:
        print("\n" + "=" * 60)
        print("游戏结束")
        print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n游戏已退出")
    except Exception as e:
        print(f"\n游戏出错: {e}")
        import traceback
        traceback.print_exc()

