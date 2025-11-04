"""
四则运算求解器
用于找到能用给定牌计算出目标值的方法
"""
from typing import List, Tuple, Optional
from card import Card


class Solver:
    """四则运算求解器"""
    
    @staticmethod
    def solve(cards: List[Card], target: int, must_use_all: bool = True, 
              exclude_card: Optional[Card] = None) -> Optional[Tuple[str, float]]:
        """
        求解能否用给定的牌计算出目标值
        
        Args:
            cards: 可用的牌列表
            target: 目标值
            must_use_all: 是否必须使用所有牌（除了exclude_card）
            exclude_card: 可选的排除牌（如黑桃K）
        
        Returns:
            如果能计算出目标值，返回(表达式字符串, 计算结果)，否则返回None
        """
        # 获取需要使用的牌的点数
        values = []
        for card in cards:
            if exclude_card and card == exclude_card:
                if not must_use_all:
                    continue  # 跳过黑桃K（如果不需要使用所有牌）
                else:
                    # 即使必须使用所有牌，黑桃K也可以选择不使用（根据规则）
                    pass
            
            # 计算牌的点数（需要上下文来计算大小王）
            numeric_value = card.get_numeric_value(cards)
            values.append((numeric_value, card))
        
        # 如果必须使用所有牌（除了可选的排除牌），确保所有牌都被使用
        if must_use_all and exclude_card:
            # 黑桃K可用可不用，所以我们可以尝试两种方式
            values_without_spade_k = [(v, c) for v, c in values if not c.is_spade_king()]
            values_with_spade_k = values
            
            # 先尝试不使用黑桃K
            result = Solver._solve_values(values_without_spade_k, target)
            if result:
                return result
            
            # 再尝试使用黑桃K
            result = Solver._solve_values(values_with_spade_k, target)
            if result:
                return result
        else:
            # 必须使用所有牌
            result = Solver._solve_values(values, target)
            if result:
                return result
        
        return None
    
    @staticmethod
    def _solve_values(values: List[Tuple[int, Card]], target: int) -> Optional[Tuple[str, float]]:
        """
        使用数值列表求解目标值
        
        Args:
            values: (数值, 牌)的列表
            target: 目标值
        
        Returns:
            如果能计算出目标值，返回(表达式字符串, 计算结果)，否则返回None
        """
        if len(values) == 0:
            return None
        
        if len(values) == 1:
            val, _ = values[0]
            if abs(val - target) < 0.0001:  # 浮点数比较
                return (str(val), float(val))
            return None
        
        # 尝试所有可能的运算组合
        # 使用递归方法，尝试所有可能的表达式
        from itertools import permutations
        
        # 获取所有数值
        nums = [v[0] for v in values]
        
        # 尝试所有排列
        for perm in permutations(nums):
            result = Solver._try_operations(list(perm), target)
            if result:
                return result
        
        return None
    
    @staticmethod
    def _try_operations(nums: List[int], target: int) -> Optional[Tuple[str, float]]:
        """
        尝试对数字列表进行运算（递归方法）
        使用表达式和值的元组列表来跟踪表达式
        
        Args:
            nums: 数字列表
            target: 目标值
        
        Returns:
            如果能计算出目标值，返回(表达式字符串, 计算结果)，否则返回None
        """
        if len(nums) == 1:
            if abs(nums[0] - target) < 0.0001:
                return (str(nums[0]), float(nums[0]))
            return None
        
        # 使用表达式和值的元组列表
        exprs = [(str(n), float(n)) for n in nums]
        
        # 递归尝试所有可能的运算
        return Solver._try_operations_helper(exprs, target)
    
    @staticmethod
    def _try_operations_helper(exprs: List[Tuple[str, float]], target: float) -> Optional[Tuple[str, float]]:
        """
        辅助函数：使用表达式列表进行运算
        
        Args:
            exprs: (表达式字符串, 值)的列表
            target: 目标值
        
        Returns:
            如果能计算出目标值，返回(表达式字符串, 计算结果)，否则返回None
        """
        if len(exprs) == 1:
            expr, val = exprs[0]
            if abs(val - target) < 0.0001:
                return (expr, val)
            return None
        
        # 对于每一对相邻的表达式，尝试四种运算
        for i in range(len(exprs) - 1):
            expr1, val1 = exprs[i]
            expr2, val2 = exprs[i + 1]
            
            for op in ['+', '-', '*', '/']:
                try:
                    if op == '+':
                        result_val = val1 + val2
                        result_expr = f"({expr1} + {expr2})"
                    elif op == '-':
                        result_val = val1 - val2
                        result_expr = f"({expr1} - {expr2})"
                    elif op == '*':
                        result_val = val1 * val2
                        result_expr = f"({expr1} * {expr2})"
                    elif op == '/':
                        if abs(val2) < 0.0001:
                            continue
                        result_val = val1 / val2
                        result_expr = f"({expr1} / {expr2})"
                    
                    # 创建新的表达式列表
                    new_exprs = exprs[:i] + [(result_expr, result_val)] + exprs[i + 2:]
                    
                    # 递归求解
                    result = Solver._try_operations_helper(new_exprs, target)
                    if result:
                        return result
                except:
                    continue
        
        return None
    
    @staticmethod
    def solve_all_combinations(cards: List[Card], target: int, 
                              exclude_card: Optional[Card] = None) -> List[Tuple[str, float]]:
        """
        找到所有可能的解法（使用不同数量的牌）
        
        Args:
            cards: 可用的牌列表
            target: 目标值
            exclude_card: 可选的排除牌（如黑桃K）
        
        Returns:
            所有可能的解法列表
        """
        solutions = []
        
        # 获取所有数值
        values = []
        for card in cards:
            if exclude_card and card == exclude_card:
                continue  # 跳过黑桃K（可选）
            numeric_value = card.get_numeric_value(cards)
            values.append((numeric_value, card))
        
        # 尝试使用不同数量的牌
        from itertools import combinations
        
        for r in range(1, len(values) + 1):
            for combo in combinations(values, r):
                # 必须使用除黑桃K外的所有牌，但黑桃K可用可不用
                # 所以我们需要检查是否使用了所有非黑桃K的牌
                non_spade_k_cards = [c for c in cards if not c.is_spade_king()]
                used_cards = [c for _, c in combo]
                
                # 如果必须使用所有牌（除了黑桃K），需要确保所有非黑桃K的牌都被使用
                if len(non_spade_k_cards) > 0:
                    all_non_spade_k_used = all(
                        any(c == used for used in used_cards) 
                        for c in non_spade_k_cards
                    )
                    if not all_non_spade_k_used:
                        continue
                
                result = Solver._solve_values(list(combo), target)
                if result:
                    solutions.append(result)
        
        return solutions

