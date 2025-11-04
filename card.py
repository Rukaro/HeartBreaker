"""
扑克牌类定义
"""
from enum import Enum
from typing import Optional


class Suit(Enum):
    """花色"""
    SPADE = "♠"  # 黑桃
    HEART = "♥"  # 红心
    DIAMOND = "♦"  # 方块
    CLUB = "♣"  # 梅花
    JOKER = "🃏"  # 王牌


class Card:
    """扑克牌"""
    
    def __init__(self, suit: Suit, value: Optional[int] = None, is_big_joker: bool = False):
        """
        初始化一张牌
        
        Args:
            suit: 花色
            value: 点数（1-13，None表示王牌）
            is_big_joker: 是否是大王（True=大王，False=小王，只有当suit是JOKER时有效）
        """
        self.suit = suit
        self.value = value
        self.is_big_joker = is_big_joker
    
    def __repr__(self):
        if self.suit == Suit.JOKER:
            return "大王" if self.is_big_joker else "小王"
        else:
            value_str = self.get_value_str()
            return f"{self.suit.value}{value_str}"
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return (self.suit == other.suit and 
                self.value == other.value and 
                self.is_big_joker == other.is_big_joker)
    
    def __hash__(self):
        return hash((self.suit, self.value, self.is_big_joker))
    
    def get_value_str(self) -> str:
        """获取点数的字符串表示"""
        if self.value == 1:
            return "A"
        elif self.value == 11:
            return "J"
        elif self.value == 12:
            return "Q"
        elif self.value == 13:
            return "K"
        else:
            return str(self.value)
    
    def get_numeric_value(self, context_cards: list['Card'] = None) -> int:
        """
        获取牌的点数（用于计算）
        
        Args:
            context_cards: 上下文中的其他牌（用于计算大小王的点数）
        
        Returns:
            牌的点数值
        """
        if self.suit == Suit.JOKER:
            if context_cards is None or len(context_cards) == 0:
                # 没有上下文，返回默认值
                return 14 if self.is_big_joker else 1
            
            # 过滤掉大小王，获取其他牌的点数
            other_cards = [c for c in context_cards if c.suit != Suit.JOKER]
            if len(other_cards) == 0:
                return 14 if self.is_big_joker else 1
            
            # 获取其他牌的点数
            other_values = []
            for card in other_cards:
                if card.value:
                    other_values.append(card.value)
            
            if len(other_values) == 0:
                return 14 if self.is_big_joker else 1
            
            if self.is_big_joker:
                # 大王 = 其他牌中最大的点数
                return max(other_values)
            else:
                # 小王 = 其他牌中最小的点数
                return min(other_values)
        else:
            return self.value if self.value else 0
    
    def is_spade_king(self) -> bool:
        """判断是否是黑桃K"""
        return self.suit == Suit.SPADE and self.value == 13
    
    def is_king(self) -> bool:
        """判断是否是K（任意花色的K）"""
        return self.value == 13 and self.suit != Suit.JOKER
    
    @staticmethod
    def create_deck() -> list['Card']:
        """创建一副完整的牌（52张标准牌 + 2张王牌）"""
        deck = []
        
        # 创建标准牌
        for suit in [Suit.SPADE, Suit.HEART, Suit.DIAMOND, Suit.CLUB]:
            for value in range(1, 14):
                deck.append(Card(suit, value))
        
        # 添加王牌
        deck.append(Card(Suit.JOKER, None, False))  # 小王
        deck.append(Card(Suit.JOKER, None, True))   # 大王
        
        return deck

