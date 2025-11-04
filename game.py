"""
游戏主逻辑
"""
import random
from typing import List, Optional
from card import Card, Suit
from solver import Solver


class Game:
    """失心王游戏"""
    
    def __init__(self):
        """初始化游戏"""
        self.deck = []
        self.hand = []  # 手牌
        self.enemies = []  # 敌人牌
        self.spade_king = None  # 黑桃K
        self.kings_defeated = 0  # 已击败的K的数量
        self.is_game_over = False
        self.is_victory = False
        
        self._initialize_game()
    
    def _initialize_game(self):
        """初始化游戏状态"""
        # 创建牌堆
        self.deck = Card.create_deck()
        
        # 找到黑桃K
        self.spade_king = next((c for c in self.deck if c.is_spade_king()), None)
        if not self.spade_king:
            raise ValueError("找不到黑桃K！")
        
        # 移除黑桃K
        self.deck.remove(self.spade_king)
        
        # 洗牌
        random.shuffle(self.deck)
        
        # 初始化手牌：黑桃K + 4张随机牌
        self.hand = [self.spade_king]
        for _ in range(4):
            if len(self.deck) > 0:
                self.hand.append(self.deck.pop(0))
        
        # 翻开4张牌作为敌人
        self._refresh_enemies()
    
    def _refresh_enemies(self):
        """刷新敌人牌（直到有4个敌人）"""
        while len(self.enemies) < 4 and len(self.deck) > 0:
            self.enemies.append(self.deck.pop(0))
    
    def get_enemy_values(self) -> List[int]:
        """获取所有敌人的点数"""
        values = []
        for enemy in self.enemies:
            # 计算敌人点数时，需要考虑上下文（敌人牌）
            value = enemy.get_numeric_value(self.enemies)
            values.append(value)
        return values
    
    def can_defeat_enemy(self, enemy_index: int) -> Optional[tuple]:
        """
        检查是否能够击败指定的敌人
        
        Args:
            enemy_index: 敌人的索引（0-3）
        
        Returns:
            如果能击败，返回(表达式字符串, 计算结果)，否则返回None
        """
        if enemy_index < 0 or enemy_index >= len(self.enemies):
            return None
        
        enemy = self.enemies[enemy_index]
        target_value = enemy.get_numeric_value(self.enemies)
        
        # 使用求解器找到解决方案
        # 除黑桃K之外的牌必须全部用到，黑桃K可用可不用
        solution = Solver.solve(
            self.hand, 
            target_value, 
            must_use_all=True, 
            exclude_card=self.spade_king
        )
        
        return solution
    
    def defeat_enemy(self, enemy_index: int, skip_validation: bool = False) -> bool:
        """
        击败指定的敌人
        
        Args:
            enemy_index: 敌人的索引
            skip_validation: 是否跳过验证（用于手动输入算式的情况）
        
        Returns:
            是否成功击败
        """
        if not skip_validation:
            solution = self.can_defeat_enemy(enemy_index)
            if not solution:
                return False
        
        enemy = self.enemies[enemy_index]
        
        # 检查是否是K
        if enemy.is_king():
            self.kings_defeated += 1
        
        # 移除敌人
        defeated_enemy = self.enemies.pop(enemy_index)
        
        # 刷新敌人牌
        self._refresh_enemies()
        
        # 将击败的敌人加入手牌
        self.hand.append(defeated_enemy)
        
        # 检查胜利条件
        if self.kings_defeated >= 3:
            self.is_game_over = True
            self.is_victory = True
        
        return True
    
    def discard_card(self, card_index: int) -> bool:
        """
        丢弃一张手牌
        
        Args:
            card_index: 手牌的索引
        
        Returns:
            是否成功丢弃（不能丢弃黑桃K）
        """
        if card_index < 0 or card_index >= len(self.hand):
            return False
        
        card = self.hand[card_index]
        
        # 不能丢弃黑桃K
        if card.is_spade_king():
            return False
        
        # 丢弃牌
        self.hand.pop(card_index)
        return True
    
    def get_game_state(self) -> dict:
        """获取游戏状态"""
        return {
            'hand': self.hand,
            'enemies': self.enemies,
            'kings_defeated': self.kings_defeated,
            'is_game_over': self.is_game_over,
            'is_victory': self.is_victory,
            'deck_size': len(self.deck)
        }

