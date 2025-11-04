// 游戏状态
let gameId = null;
let gameState = null;
let selectedEnemyIndex = null;
let waitingForDiscard = false;

// API基础URL
const API_BASE = '';

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    // 绑定事件
    document.getElementById('new-game-btn').addEventListener('click', startNewGame);
    document.getElementById('refresh-btn').addEventListener('click', refreshGameState);
    document.getElementById('confirm-attack-btn').addEventListener('click', confirmAttack);
    document.getElementById('cancel-attack-btn').addEventListener('click', cancelAttack);
    document.getElementById('cancel-discard-btn').addEventListener('click', cancelDiscard);
    document.getElementById('restart-btn').addEventListener('click', startNewGame);
    
    // 攻击选择相关
    document.getElementById('auto-calculate-btn').addEventListener('click', handleAutoCalculate);
    document.getElementById('manual-input-btn').addEventListener('click', handleManualInput);
    document.getElementById('cancel-choice-btn').addEventListener('click', cancelChoice);
    
    // 手动输入相关
    document.getElementById('validate-expression-btn').addEventListener('click', validateManualExpression);
    document.getElementById('confirm-manual-attack-btn').addEventListener('click', confirmManualAttack);
    document.getElementById('cancel-manual-btn').addEventListener('click', cancelManualInput);
    
    // 输入框回车键支持
    document.getElementById('expression-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            validateManualExpression();
        }
    });

    // 启动新游戏
    startNewGame();
});

// 显示消息
function showMessage(text, type = 'info') {
    const messageEl = document.getElementById('message');
    messageEl.textContent = text;
    messageEl.className = `message ${type}`;
    messageEl.style.display = 'block';
    
    setTimeout(() => {
        messageEl.style.display = 'none';
    }, 3000);
}

// 启动新游戏
async function startNewGame() {
    try {
        const response = await fetch(`${API_BASE}/api/game/new`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error('创建游戏失败');
        }
        
        const data = await response.json();
        gameId = data.game_id;
        gameState = data;
        waitingForDiscard = false;
        
        updateUI();
        showMessage('新游戏已开始！', 'success');
    } catch (error) {
        console.error('Error:', error);
        showMessage('创建游戏失败: ' + error.message, 'error');
    }
}

// 刷新游戏状态
async function refreshGameState() {
    if (!gameId) {
        showMessage('请先开始新游戏', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/game/${gameId}/state`);
        
        if (!response.ok) {
            throw new Error('获取游戏状态失败');
        }
        
        const data = await response.json();
        gameState = data;
        
        updateUI();
        showMessage('游戏状态已刷新', 'info');
    } catch (error) {
        console.error('Error:', error);
        showMessage('刷新失败: ' + error.message, 'error');
    }
}

// 更新UI
function updateUI() {
    if (!gameState) return;
    
    // 更新游戏信息
    document.getElementById('kings-defeated').textContent = gameState.kings_defeated;
    document.getElementById('deck-size').textContent = gameState.deck_size;
    
    // 更新敌人牌
    renderEnemies();
    
    // 更新手牌
    renderHand();
    
    // 检查游戏是否结束
    if (gameState.is_game_over) {
        if (gameState.is_victory) {
            showGameOverModal('🎉 恭喜！你成功击败了所有三个K！', '游戏胜利！');
        } else {
            showGameOverModal('游戏结束', '你没有击败所有三个K');
        }
    }
    
    // 隐藏所有区域（如果不是相应状态）
    if (!waitingForDiscard) {
        document.getElementById('solution-section').style.display = 'none';
        document.getElementById('discard-section').style.display = 'none';
        document.getElementById('attack-choice-section').style.display = 'none';
        document.getElementById('manual-input-section').style.display = 'none';
    }
}

// 显示手牌点数
function displayHandValues() {
    if (!gameState || !gameState.hand) return;
    
    const container = document.getElementById('hand-values-display');
    container.innerHTML = '';
    
    // 获取手牌点数（需要从后端获取）
    // 这里我们显示手牌的基本信息
    gameState.hand.forEach((card, index) => {
        const item = document.createElement('div');
        item.className = 'hand-value-item';
        
        // 计算点数（简化处理，实际应该从后端获取）
        let value = card.value;
        if (card.value === 1) value = 'A';
        else if (card.value === 11) value = 'J';
        else if (card.value === 12) value = 'Q';
        else if (card.value === 13) value = 'K';
        
        item.textContent = `${card.display} = ${getCardNumericValue(card)}`;
        if (card.is_spade_king) {
            item.style.borderColor = '#ffd700';
            item.style.color = '#ffd700';
        }
        container.appendChild(item);
    });
}

// 获取牌的点数（简化版，实际应该从后端获取准确值）
function getCardNumericValue(card) {
    // 这里返回卡牌的基本值，实际大小王的点数需要根据上下文计算
    if (card.suit === 'JOKER') {
        return card.is_big_joker ? '大王' : '小王';
    }
    return card.value || 0;
}

// 渲染敌人牌
function renderEnemies() {
    const container = document.getElementById('enemies-container');
    container.innerHTML = '';
    
    if (!gameState || !gameState.enemies) return;
    
    gameState.enemies.forEach((enemy, index) => {
        const card = document.createElement('div');
        card.className = 'card enemy-card';
        card.dataset.index = index;
        
        const value = gameState.enemy_values[index];
        const isKing = enemy.is_king;
        
        card.innerHTML = `
            <div class="card-value">${enemy.display}</div>
            <div class="card-label">敌人 ${index + 1}</div>
            <div class="card-point">点数: ${value}</div>
            ${isKing ? '<div class="card-label" style="color: #ffd700;">K</div>' : ''}
        `;
        
        // 检查是否可以攻击
        checkEnemyAttackable(index).then(canAttack => {
            if (canAttack) {
                card.classList.add('attackable');
            }
        });
        
        card.addEventListener('click', () => attackEnemy(index));
        container.appendChild(card);
    });
}

// 渲染手牌
function renderHand() {
    const container = document.getElementById('hand-container');
    container.innerHTML = '';
    
    if (!gameState || !gameState.hand) return;
    
    gameState.hand.forEach((card, index) => {
        const cardEl = document.createElement('div');
        cardEl.className = 'card hand-card';
        cardEl.dataset.index = index;
        
        if (card.is_spade_king) {
            cardEl.classList.add('spade-king');
        }
        
        cardEl.innerHTML = `
            <div class="card-value">${card.display}</div>
            ${card.is_spade_king ? '<div class="card-label" style="color: #ffd700;">黑桃K</div>' : ''}
        `;
        
        container.appendChild(cardEl);
    });
}

// 检查敌人是否可以攻击
async function checkEnemyAttackable(enemyIndex) {
    if (!gameId) return false;
    
    try {
        const response = await fetch(`${API_BASE}/api/game/${gameId}/check-enemy`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ enemy_index: enemyIndex })
        });
        
        if (!response.ok) {
            return false;
        }
        
        const data = await response.json();
        return data.can_defeat;
    } catch (error) {
        console.error('Error:', error);
        return false;
    }
}

// 攻击敌人
async function attackEnemy(enemyIndex) {
    if (!gameId || waitingForDiscard) return;
    
    selectedEnemyIndex = enemyIndex;
    
    // 获取敌人点数
    try {
        const stateResponse = await fetch(`${API_BASE}/api/game/${gameId}/state`);
        if (stateResponse.ok) {
            const stateData = await stateResponse.json();
            const targetValue = stateData.enemy_values[enemyIndex];
            
            // 显示攻击选择界面
            document.getElementById('choice-target-value').textContent = targetValue;
            document.getElementById('attack-choice-section').style.display = 'block';
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage('获取敌人信息失败', 'error');
    }
}

// 处理自动计算
async function handleAutoCalculate() {
    if (selectedEnemyIndex === null) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/game/${gameId}/check-enemy`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ enemy_index: selectedEnemyIndex })
        });
        
        if (!response.ok) {
            throw new Error('检查敌人失败');
        }
        
        const data = await response.json();
        
        if (!data.can_defeat) {
            showMessage('无法用当前手牌计算出该敌人的点数', 'error');
            document.getElementById('attack-choice-section').style.display = 'none';
            return;
        }
        
        // 隐藏选择界面，显示解决方案
        document.getElementById('attack-choice-section').style.display = 'none';
        document.getElementById('target-value').textContent = data.target_value;
        document.getElementById('expression').textContent = data.expression;
        document.getElementById('result').textContent = data.result;
        document.getElementById('solution-section').style.display = 'block';
        
    } catch (error) {
        console.error('Error:', error);
        showMessage('攻击失败: ' + error.message, 'error');
    }
}

// 处理手动输入
async function handleManualInput() {
    if (selectedEnemyIndex === null) return;
    
    // 获取敌人点数和手牌信息
    try {
        const stateResponse = await fetch(`${API_BASE}/api/game/${gameId}/state`);
        if (!stateResponse.ok) {
            throw new Error('获取游戏状态失败');
        }
        
        const stateData = await stateResponse.json();
        const targetValue = stateData.enemy_values[selectedEnemyIndex];
        
        // 隐藏选择界面，显示手动输入界面
        document.getElementById('attack-choice-section').style.display = 'none';
        document.getElementById('manual-target-value').textContent = targetValue;
        
        // 显示手牌点数（需要从后端获取准确的点数）
        await displayHandValuesWithNumericValues(stateData);
        
        document.getElementById('manual-input-section').style.display = 'block';
        document.getElementById('expression-input').focus();
        
    } catch (error) {
        console.error('Error:', error);
        showMessage('获取游戏信息失败', 'error');
    }
}

// 显示手牌点数（带实际数值）
async function displayHandValuesWithNumericValues(stateData) {
    const container = document.getElementById('hand-values-display');
    container.innerHTML = '';
    
    // 从后端获取手牌的实际点数
    try {
        const response = await fetch(`${API_BASE}/api/game/${gameId}/hand-values`);
        if (!response.ok) {
            throw new Error('获取手牌点数失败');
        }
        
        const data = await response.json();
        
        data.hand_values.forEach((item) => {
            const card = item.card;
            const numericValue = item.numeric_value;
            
            const cardEl = document.createElement('div');
            cardEl.className = 'hand-value-item';
            
            let displayText = `${card.display} = ${numericValue}`;
            if (card.is_spade_king) {
                displayText += ' (可选)';
                cardEl.style.borderColor = '#ffd700';
                cardEl.style.color = '#ffd700';
            }
            
            cardEl.textContent = displayText;
            container.appendChild(cardEl);
        });
    } catch (error) {
        console.error('Error:', error);
        // 如果获取失败，显示基本信息
        stateData.hand.forEach((card) => {
            const item = document.createElement('div');
            item.className = 'hand-value-item';
            
            let displayText = `${card.display}`;
            if (card.is_spade_king) {
                displayText += ' (可选)';
                item.style.borderColor = '#ffd700';
                item.style.color = '#ffd700';
            }
            
            item.textContent = displayText;
            container.appendChild(item);
        });
    }
}

// 取消选择
function cancelChoice() {
    selectedEnemyIndex = null;
    document.getElementById('attack-choice-section').style.display = 'none';
}

// 取消手动输入
function cancelManualInput() {
    selectedEnemyIndex = null;
    document.getElementById('manual-input-section').style.display = 'none';
    document.getElementById('expression-input').value = '';
    document.getElementById('manual-validation-result').style.display = 'none';
    document.getElementById('confirm-manual-attack-btn').style.display = 'none';
}

// 验证手动输入的算式
async function validateManualExpression() {
    if (!gameId || selectedEnemyIndex === null) return;
    
    const expression = document.getElementById('expression-input').value.trim();
    if (!expression) {
        showMessage('请输入算式', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/game/${gameId}/validate-expression`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                enemy_index: selectedEnemyIndex,
                expression: expression
            })
        });
        
        if (!response.ok) {
            throw new Error('验证算式失败');
        }
        
        const data = await response.json();
        const resultDiv = document.getElementById('manual-validation-result');
        
        if (data.valid) {
            resultDiv.className = 'manual-validation-result success';
            resultDiv.textContent = `✓ 算式有效！计算结果: ${data.result} = 目标点数 ${data.target_value}`;
            resultDiv.style.display = 'block';
            document.getElementById('confirm-manual-attack-btn').style.display = 'inline-block';
        } else {
            resultDiv.className = 'manual-validation-result error';
            resultDiv.textContent = `✗ ${data.error || '算式无效'}`;
            resultDiv.style.display = 'block';
            document.getElementById('confirm-manual-attack-btn').style.display = 'none';
        }
        
    } catch (error) {
        console.error('Error:', error);
        showMessage('验证失败: ' + error.message, 'error');
    }
}

// 确认手动攻击
async function confirmManualAttack() {
    if (!gameId || selectedEnemyIndex === null) return;
    
    const expression = document.getElementById('expression-input').value.trim();
    if (!expression) {
        showMessage('请输入算式', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/game/${gameId}/defeat-enemy`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                enemy_index: selectedEnemyIndex,
                skip_validation: true,
                expression: expression
            })
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || '击败敌人失败');
        }
        
        const data = await response.json();
        gameState = data;
        selectedEnemyIndex = null;
        waitingForDiscard = false;
        
        // 隐藏手动输入界面
        document.getElementById('manual-input-section').style.display = 'none';
        document.getElementById('expression-input').value = '';
        document.getElementById('manual-validation-result').style.display = 'none';
        document.getElementById('confirm-manual-attack-btn').style.display = 'none';
        
        updateUI();
        showMessage('成功击败敌人！', 'success');
        
        // 检查胜利
        if (data.is_victory) {
            return;
        }
        
        // 显示丢弃手牌区域
        showDiscardSection();
        
    } catch (error) {
        console.error('Error:', error);
        showMessage('攻击失败: ' + error.message, 'error');
    }
}

// 确认攻击
async function confirmAttack() {
    if (!gameId || selectedEnemyIndex === null) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/game/${gameId}/defeat-enemy`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ enemy_index: selectedEnemyIndex })
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || '击败敌人失败');
        }
        
        const data = await response.json();
        gameState = data;
        selectedEnemyIndex = null;
        
        // 隐藏解决方案区域
        document.getElementById('solution-section').style.display = 'none';
        
        // 检查是否胜利
        if (data.is_victory) {
            updateUI();
            return;
        }
        
        // 显示丢弃手牌区域
        showDiscardSection();
        
    } catch (error) {
        console.error('Error:', error);
        showMessage('攻击失败: ' + error.message, 'error');
    }
}

// 取消攻击
function cancelAttack() {
    selectedEnemyIndex = null;
    document.getElementById('solution-section').style.display = 'none';
}

// 显示丢弃手牌区域
function showDiscardSection() {
    waitingForDiscard = true;
    const container = document.getElementById('discard-container');
    container.innerHTML = '';
    
    // 获取可丢弃的手牌（不包括黑桃K）
    const discardableCards = gameState.hand.filter((card, index) => !card.is_spade_king);
    
    if (discardableCards.length === 0) {
        showMessage('没有可丢弃的手牌', 'error');
        waitingForDiscard = false;
        updateUI();
        return;
    }
    
    // 找到可丢弃手牌在原手牌中的索引
    discardableCards.forEach((card) => {
        const originalIndex = gameState.hand.findIndex(c => 
            c.suit === card.suit && 
            c.value === card.value && 
            c.is_big_joker === card.is_big_joker
        );
        
        const cardEl = document.createElement('div');
        cardEl.className = 'card hand-card discardable';
        cardEl.dataset.index = originalIndex;
        
        cardEl.innerHTML = `
            <div class="card-value">${card.display}</div>
        `;
        
        cardEl.addEventListener('click', () => discardCard(originalIndex));
        container.appendChild(cardEl);
    });
    
    document.getElementById('discard-section').style.display = 'block';
}

// 丢弃手牌
async function discardCard(cardIndex) {
    if (!gameId) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/game/${gameId}/discard`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ card_index: cardIndex })
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || '丢弃手牌失败');
        }
        
        const data = await response.json();
        gameState = data;
        waitingForDiscard = false;
        
        // 隐藏丢弃区域
        document.getElementById('discard-section').style.display = 'none';
        
        updateUI();
        showMessage('已丢弃手牌', 'success');
        
    } catch (error) {
        console.error('Error:', error);
        showMessage('丢弃失败: ' + error.message, 'error');
    }
}

// 取消丢弃
function cancelDiscard() {
    waitingForDiscard = false;
    document.getElementById('discard-section').style.display = 'none';
    showMessage('已取消丢弃', 'info');
}

// 显示游戏结束模态框
function showGameOverModal(title, message) {
    document.getElementById('game-over-title').textContent = title;
    document.getElementById('game-over-message').textContent = message;
    document.getElementById('game-over-modal').style.display = 'flex';
}

