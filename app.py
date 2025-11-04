"""
失心王游戏 - Flask Web应用
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
from game import Game
from card import Card, Suit

app = Flask(__name__)
CORS(app)

# 存储游戏实例（简单的单用户实现）
games = {}

def card_to_dict(card: Card) -> dict:
    """将Card对象转换为字典"""
    return {
        'suit': card.suit.value if card.suit != Suit.JOKER else 'JOKER',
        'value': card.value,
        'is_big_joker': card.is_big_joker if card.suit == Suit.JOKER else False,
        'display': str(card),
        'is_spade_king': card.is_spade_king(),
        'is_king': card.is_king()
    }

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/game/new', methods=['POST'])
def new_game():
    """创建新游戏"""
    game = Game()
    game_id = str(id(game))
    games[game_id] = game
    
    state = game.get_game_state()
    enemy_values = game.get_enemy_values()
    
    return jsonify({
        'game_id': game_id,
        'hand': [card_to_dict(card) for card in state['hand']],
        'enemies': [card_to_dict(card) for card in state['enemies']],
        'enemy_values': enemy_values,
        'kings_defeated': state['kings_defeated'],
        'is_game_over': state['is_game_over'],
        'is_victory': state['is_victory'],
        'deck_size': state['deck_size']
    })

@app.route('/api/game/<game_id>/state', methods=['GET'])
def get_game_state(game_id):
    """获取游戏状态"""
    if game_id not in games:
        return jsonify({'error': '游戏不存在'}), 404
    
    game = games[game_id]
    state = game.get_game_state()
    enemy_values = game.get_enemy_values()
    
    return jsonify({
        'hand': [card_to_dict(card) for card in state['hand']],
        'enemies': [card_to_dict(card) for card in state['enemies']],
        'enemy_values': enemy_values,
        'kings_defeated': state['kings_defeated'],
        'is_game_over': state['is_game_over'],
        'is_victory': state['is_victory'],
        'deck_size': state['deck_size']
    })

@app.route('/api/game/<game_id>/check-enemy', methods=['POST'])
def check_enemy(game_id):
    """检查是否能击败敌人"""
    if game_id not in games:
        return jsonify({'error': '游戏不存在'}), 404
    
    data = request.get_json()
    enemy_index = data.get('enemy_index')
    
    if enemy_index is None:
        return jsonify({'error': '缺少enemy_index参数'}), 400
    
    game = games[game_id]
    solution = game.can_defeat_enemy(enemy_index)
    
    if solution:
        enemy = game.enemies[enemy_index]
        enemy_value = enemy.get_numeric_value(game.enemies)
        return jsonify({
            'can_defeat': True,
            'expression': solution[0],
            'result': solution[1],
            'target_value': enemy_value
        })
    else:
        return jsonify({
            'can_defeat': False
        })

@app.route('/api/game/<game_id>/defeat-enemy', methods=['POST'])
def defeat_enemy(game_id):
    """击败敌人"""
    if game_id not in games:
        return jsonify({'error': '游戏不存在'}), 404
    
    data = request.get_json()
    enemy_index = data.get('enemy_index')
    skip_validation = data.get('skip_validation', False)  # 手动输入时跳过自动验证
    
    if enemy_index is None:
        return jsonify({'error': '缺少enemy_index参数'}), 400
    
    game = games[game_id]
    
    # 如果跳过验证，需要先验证手动输入的算式
    if skip_validation:
        expression = data.get('expression')
        if not expression:
            return jsonify({'error': '手动输入时需要提供算式'}), 400
        
        # 验证算式
        try:
            result = eval(expression)
            enemy = game.enemies[enemy_index]
            target_value = enemy.get_numeric_value(game.enemies)
            
            if abs(result - target_value) > 0.0001:
                return jsonify({'error': '算式计算结果不正确'}), 400
        except:
            return jsonify({'error': '算式无效'}), 400
    
    success = game.defeat_enemy(enemy_index, skip_validation=skip_validation)
    
    if not success:
        return jsonify({'error': '无法击败该敌人'}), 400
    
    state = game.get_game_state()
    enemy_values = game.get_enemy_values()
    
    return jsonify({
        'success': True,
        'hand': [card_to_dict(card) for card in state['hand']],
        'enemies': [card_to_dict(card) for card in state['enemies']],
        'enemy_values': enemy_values,
        'kings_defeated': state['kings_defeated'],
        'is_game_over': state['is_game_over'],
        'is_victory': state['is_victory'],
        'deck_size': state['deck_size']
    })

@app.route('/api/game/<game_id>/hand-values', methods=['GET'])
def get_hand_values(game_id):
    """获取手牌的实际点数"""
    if game_id not in games:
        return jsonify({'error': '游戏不存在'}), 404
    
    game = games[game_id]
    hand_values = []
    
    for card in game.hand:
        numeric_value = card.get_numeric_value(game.hand)
        hand_values.append({
            'card': card_to_dict(card),
            'numeric_value': numeric_value
        })
    
    return jsonify({'hand_values': hand_values})

@app.route('/api/game/<game_id>/validate-expression', methods=['POST'])
def validate_expression(game_id):
    """验证用户输入的算式"""
    if game_id not in games:
        return jsonify({'error': '游戏不存在'}), 404
    
    data = request.get_json()
    enemy_index = data.get('enemy_index')
    expression = data.get('expression')
    
    if enemy_index is None or expression is None:
        return jsonify({'error': '缺少参数'}), 400
    
    game = games[game_id]
    
    if enemy_index < 0 or enemy_index >= len(game.enemies):
        return jsonify({'error': '无效的敌人索引'}), 400
    
    enemy = game.enemies[enemy_index]
    target_value = enemy.get_numeric_value(game.enemies)
    
    # 获取手牌的点数
    hand_values = {}
    for card in game.hand:
        numeric_value = card.get_numeric_value(game.hand)
        # 使用卡片作为key，存储点数
        card_key = f"{card.suit.value}_{card.value}_{card.is_big_joker}"
        hand_values[card_key] = numeric_value
        # 也存储数值本身，用于查找
        if numeric_value not in hand_values:
            hand_values[numeric_value] = []
        if not isinstance(hand_values[numeric_value], list):
            hand_values[numeric_value] = []
        hand_values[numeric_value].append(card_key)
    
    # 解析并验证算式
    try:
        # 安全地计算表达式
        result = eval(expression)
        
        # 检查结果是否等于目标值
        if abs(result - target_value) > 0.0001:
            return jsonify({
                'valid': False,
                'error': f'计算结果 {result} 不等于目标点数 {target_value}'
            })
        
        # 提取表达式中使用的数字
        import re
        # 匹配数字（包括小数）
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
            return jsonify({
                'valid': False,
                'error': f'未使用所有必须的手牌（缺少点数: {missing_cards}）'
            })
        
        # 检查使用的数字是否都在手牌中
        # 允许使用黑桃K的点数（13），但不强制
        spade_king_value = game.spade_king.get_numeric_value(game.hand) if game.spade_king else None
        
        invalid_values = []
        for used_val in used_values:
            # 检查是否在手牌的点数中
            valid = False
            for card in game.hand:
                card_val = card.get_numeric_value(game.hand)
                if abs(card_val - used_val) < 0.0001:
                    valid = True
                    break
            if not valid:
                invalid_values.append(used_val)
        
        if invalid_values:
            return jsonify({
                'valid': False,
                'error': f'使用了不在手牌中的点数: {invalid_values}'
            })
        
        return jsonify({
            'valid': True,
            'result': result,
            'target_value': target_value
        })
        
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': f'算式无效: {str(e)}'
        })

@app.route('/api/game/<game_id>/discard', methods=['POST'])
def discard_card(game_id):
    """丢弃手牌"""
    if game_id not in games:
        return jsonify({'error': '游戏不存在'}), 404
    
    data = request.get_json()
    card_index = data.get('card_index')
    
    if card_index is None:
        return jsonify({'error': '缺少card_index参数'}), 400
    
    game = games[game_id]
    success = game.discard_card(card_index)
    
    if not success:
        return jsonify({'error': '无法丢弃该牌'}), 400
    
    state = game.get_game_state()
    enemy_values = game.get_enemy_values()
    
    return jsonify({
        'success': True,
        'hand': [card_to_dict(card) for card in state['hand']],
        'enemies': [card_to_dict(card) for card in state['enemies']],
        'enemy_values': enemy_values,
        'kings_defeated': state['kings_defeated'],
        'is_game_over': state['is_game_over'],
        'is_victory': state['is_victory'],
        'deck_size': state['deck_size']
    })

if __name__ == '__main__':
    import os
    # 生产环境从环境变量读取配置，开发环境使用默认值
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug, host=host, port=port)

