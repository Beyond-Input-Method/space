// 计算器状态管理
class Calculator {
    constructor() {
        this.currentInput = '0';
        this.previousInput = '';
        this.operator = null;
        this.shouldResetInput = false;
        this.expression = '';
        
        // 获取DOM元素
        this.resultDisplay = document.getElementById('result');
        this.expressionDisplay = document.getElementById('expression');
        
        // 初始化键盘事件
        this.initKeyboardEvents();
        
        // 初始化触摸事件
        this.initTouchEvents();
    }
    
    // 更新显示
    updateDisplay() {
        this.resultDisplay.textContent = this.formatNumber(this.currentInput);
        this.expressionDisplay.textContent = this.expression;
    }
    
    // 格式化数字显示
    formatNumber(num) {
        if (num === '') return '0';
        
        // 处理小数点
        if (num.includes('.')) {
            const [integer, decimal] = num.split('.');
            if (integer.length > 10) {
                return this.toScientificNotation(parseFloat(num));
            }
            return integer.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + '.' + decimal;
        }
        
        // 处理整数
        if (num.length > 10) {
            return this.toScientificNotation(parseFloat(num));
        }
        
        return num.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
    
    // 科学计数法
    toScientificNotation(num) {
        return num.toExponential(5);
    }
    
    // 输入数字
    inputNumber(number) {
        if (this.shouldResetInput) {
            this.currentInput = '';
            this.shouldResetInput = false;
        }
        
        if (this.currentInput === '0') {
            this.currentInput = number;
        } else {
            // 限制输入长度
            if (this.currentInput.replace(/[,\.]/g, '').length < 10) {
                this.currentInput += number;
            }
        }
        
        this.updateDisplay();
    }
    
    // 输入小数点
    inputDecimal() {
        if (this.shouldResetInput) {
            this.currentInput = '0';
            this.shouldResetInput = false;
        }
        
        if (!this.currentInput.includes('.')) {
            this.currentInput += '.';
            this.updateDisplay();
        }
    }
    
    // 输入操作符
    inputOperator(nextOperator) {
        const inputValue = parseFloat(this.currentInput.replace(/,/g, ''));
        
        if (this.previousInput === '') {
            this.previousInput = this.currentInput;
        } else if (this.operator && !this.shouldResetInput) {
            const result = this.performCalculation();
            this.currentInput = String(result);
            this.previousInput = this.currentInput;
            this.updateDisplay();
        }
        
        this.operator = nextOperator;
        this.shouldResetInput = true;
        
        // 更新表达式显示
        const operatorSymbol = this.getOperatorSymbol(nextOperator);
        this.expression = `${this.formatNumber(this.previousInput)} ${operatorSymbol}`;
        this.updateDisplay();
    }
    
    // 获取操作符显示符号
    getOperatorSymbol(operator) {
        switch (operator) {
            case '+': return '+';
            case '-': return '-';
            case '*': return '×';
            case '/': return '÷';
            case '%': return '%';
            default: return operator;
        }
    }
    
    // 执行计算
    performCalculation() {
        const prev = parseFloat(this.previousInput.replace(/,/g, ''));
        const current = parseFloat(this.currentInput.replace(/,/g, ''));
        
        if (isNaN(prev) || isNaN(current)) return current;
        
        let result;
        switch (this.operator) {
            case '+':
                result = prev + current;
                break;
            case '-':
                result = prev - current;
                break;
            case '*':
                result = prev * current;
                break;
            case '/':
                if (current === 0) {
                    this.showError('除数不能为零');
                    return 0;
                }
                result = prev / current;
                break;
            case '%':
                result = prev % current;
                break;
            default:
                return current;
        }
        
        // 处理计算结果
        if (!isFinite(result)) {
            this.showError('计算结果超出范围');
            return 0;
        }
        
        // 保留精度，避免浮点数精度问题
        return Math.round(result * 1000000000) / 1000000000;
    }
    
    // 计算并显示结果
    calculate() {
        if (this.operator && this.previousInput !== '' && !this.shouldResetInput) {
            const result = this.performCalculation();
            
            // 更新表达式显示
            const operatorSymbol = this.getOperatorSymbol(this.operator);
            this.expression = `${this.formatNumber(this.previousInput)} ${operatorSymbol} ${this.formatNumber(this.currentInput)} =`;
            
            this.currentInput = String(result);
            this.operator = null;
            this.previousInput = '';
            this.shouldResetInput = true;
            this.updateDisplay();
        }
    }
    
    // 清除所有
    clearAll() {
        this.currentInput = '0';
        this.previousInput = '';
        this.operator = null;
        this.shouldResetInput = false;
        this.expression = '';
        this.updateDisplay();
    }
    
    // 清除当前输入
    clearEntry() {
        this.currentInput = '0';
        this.updateDisplay();
    }
    
    // 退格
    backspace() {
        if (this.shouldResetInput) {
            return;
        }
        
        if (this.currentInput.length > 1) {
            this.currentInput = this.currentInput.slice(0, -1);
        } else {
            this.currentInput = '0';
        }
        
        this.updateDisplay();
    }
    
    // 显示错误
    showError(message) {
        this.expression = message;
        this.updateDisplay();
        
        // 2秒后清除错误信息
        setTimeout(() => {
            this.clearAll();
        }, 2000);
    }
    
    // 初始化键盘事件
    initKeyboardEvents() {
        document.addEventListener('keydown', (event) => {
            event.preventDefault();
            
            const key = event.key;
            
            // 数字键
            if (/[0-9]/.test(key)) {
                this.inputNumber(key);
            }
            // 操作符
            else if (key === '+') {
                this.inputOperator('+');
            }
            else if (key === '-') {
                this.inputOperator('-');
            }
            else if (key === '*') {
                this.inputOperator('*');
            }
            else if (key === '/') {
                this.inputOperator('/');
            }
            else if (key === '%') {
                this.inputOperator('%');
            }
            // 小数点
            else if (key === '.' || key === ',') {
                this.inputDecimal();
            }
            // 等号和回车
            else if (key === '=' || key === 'Enter') {
                this.calculate();
            }
            // 退格
            else if (key === 'Backspace') {
                this.backspace();
            }
            // 清除
            else if (key === 'Escape' || key === 'c' || key === 'C') {
                this.clearAll();
            }
            // Delete键清除当前输入
            else if (key === 'Delete') {
                this.clearEntry();
            }
        });
    }
    
    // 初始化触摸事件（简化版，减少事件阻止）
    initTouchEvents() {
        // 防止长按菜单
        document.addEventListener('contextmenu', function(event) {
            event.preventDefault();
        });
        
        // 减少事件阻止，只在必要时使用
        // 注释掉可能干扰WebBrowser的事件处理
        /*
        document.addEventListener('touchmove', function(event) {
            event.preventDefault();
        }, { passive: false });
        */
    }
}

// 创建计算器实例
let calculator = null;

// 初始化计算器
function initCalculator() {
    calculator = new Calculator();
    console.log('计算器初始化完成');
}

// 全局函数，供HTML调用（保留兼容性）
function inputNumber(number) {
    if (calculator) {
        calculator.inputNumber(number);
        addButtonFeedback();
    }
}

function inputOperator(operator) {
    if (calculator) {
        calculator.inputOperator(operator);
        addButtonFeedback();
    }
}

function inputDecimal() {
    if (calculator) {
        calculator.inputDecimal();
        addButtonFeedback();
    }
}

function calculate() {
    if (calculator) {
        calculator.calculate();
        addButtonFeedback();
    }
}

function clearAll() {
    if (calculator) {
        calculator.clearAll();
        addButtonFeedback();
    }
}

function clearEntry() {
    if (calculator) {
        calculator.clearEntry();
        addButtonFeedback();
    }
}

function backspace() {
    if (calculator) {
        calculator.backspace();
        addButtonFeedback();
    }
}

// 处理按钮点击事件
function handleButtonClick(action, value) {
    console.log('按钮点击:', action, value);
    
    if (!calculator) {
        console.error('计算器未初始化');
        return;
    }
    
    try {
        switch(action) {
            case 'number':
                calculator.inputNumber(value);
                break;
            case 'operator':
                calculator.inputOperator(value);
                break;
            case 'decimal':
                calculator.inputDecimal();
                break;
            case 'calculate':
                calculator.calculate();
                break;
            case 'clear':
                calculator.clearAll();
                break;
            case 'clear-entry':
                calculator.clearEntry();
                break;
            case 'backspace':
                calculator.backspace();
                break;
            default:
                console.warn('未知操作:', action);
        }
        
        addButtonFeedback();
    } catch (error) {
        console.error('按钮操作错误:', error);
    }
}

// 按钮反馈效果
function addButtonFeedback() {
    // 触觉反馈（如果支持）
    if ('vibrate' in navigator) {
        navigator.vibrate(5); // 减少振动时间
    }
}

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM加载完成，开始初始化计算器');
    
    // 初始化计算器
    initCalculator();
    
    // 使用事件委托处理按钮点击
    const buttonsContainer = document.querySelector('.buttons');
    if (buttonsContainer) {
        buttonsContainer.addEventListener('click', function(event) {
            const button = event.target;
            if (button.tagName === 'BUTTON') {
                const action = button.getAttribute('data-action');
                const value = button.getAttribute('data-value');
                
                console.log('按钮被点击:', button.textContent, '操作:', action, '值:', value);
                
                // 按钮视觉反馈
                button.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    button.style.transform = '';
                }, 150);
                
                // 处理操作
                handleButtonClick(action, value);
                
                // 阻止事件冒泡
                event.stopPropagation();
                event.preventDefault();
            }
        });
        
        // 添加触摸反馈（不阻止点击事件）
        buttonsContainer.addEventListener('touchstart', function(event) {
            const button = event.target;
            if (button.tagName === 'BUTTON') {
                button.style.transform = 'scale(0.95)';
            }
        });
        
        buttonsContainer.addEventListener('touchend', function(event) {
            const button = event.target;
            if (button.tagName === 'BUTTON') {
                setTimeout(() => {
                    button.style.transform = '';
                }, 150);
            }
        });
        
        console.log('事件委托设置完成');
    } else {
        console.error('未找到按钮容器');
    }
    
    console.log('全屏计算器初始化完成！');
});

// 处理页面可见性变化
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // 页面隐藏时保存状态
        try {
            localStorage.setItem('calculatorState', JSON.stringify({
                currentInput: calculator.currentInput,
                previousInput: calculator.previousInput,
                operator: calculator.operator,
                expression: calculator.expression
            }));
        } catch (e) {
            // 忽略存储错误
        }
    } else {
        // 页面显示时恢复状态
        try {
            const savedState = localStorage.getItem('calculatorState');
            if (savedState) {
                const state = JSON.parse(savedState);
                calculator.currentInput = state.currentInput || '0';
                calculator.previousInput = state.previousInput || '';
                calculator.operator = state.operator || null;
                calculator.expression = state.expression || '';
                calculator.updateDisplay();
            }
        } catch (e) {
            // 忽略恢复错误
        }
    }
});

// 处理屏幕旋转
window.addEventListener('orientationchange', function() {
    setTimeout(() => {
        calculator.updateDisplay();
        // 强制重新计算布局
        document.body.style.height = window.innerHeight + 'px';
    }, 100);
});

// 处理窗口大小变化
window.addEventListener('resize', function() {
    // 确保计算器始终铺满屏幕
    document.body.style.height = window.innerHeight + 'px';
});

// 初始设置页面高度
document.body.style.height = window.innerHeight + 'px';