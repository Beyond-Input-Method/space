/**
 * 算术表达式计算过滤器 - Arithmetic Calculator Filter
 * 
 * 功能:检测前置文本(external context)中的算术表达式,自动计算并添加到候选项列表
 * 
 * 使用场景:
 * 1. 用户在外部输入框输入: "8084+9"
 * 2. 切换到RIME输入任意内容(如拼音)
 * 3. Filter自动识别前置文本中的表达式,在候选列表顶部添加计算结果
 * 
 * 与 Translator 版本的区别:
 * - Translator: 只能处理当前输入中的表达式
 * - Filter: 可以处理前置文本中的表达式,不受segment限制
 * 
 * @author librime-qjs
 * @version 1.0.0
 */

export class ArithmeticFilter {
  constructor(env) {
    console.log("[ArithmeticFilter] 初始化算术表达式过滤器");
    this.namespace = env.namespace;

    // 验证表达式是否包含运算符
    this.hasOperatorPattern = /[+\-*/]/;
    
    // 有效的表达式字符集合
    this.validExprChars = new Set('0123456789+-*/().');

    console.log("[ArithmeticFilter] 初始化完成");
  }

  /**
   * 从文本中提取最右边的算术表达式
   * @param {string} text - 输入文本
   * @returns {Object|null} - {expr: 表达式, startPos: 开始位置, endPos: 结束位置} 或 null
   */
  extractExpression(text) {
    console.log(`[ArithmeticFilter] --- extractExpression 开始 ---`);
    console.log(`[ArithmeticFilter] 输入文本: "${text}"`);

    if (!text) {
      console.log(`[ArithmeticFilter] ❌ 文本为空`);
      return null;
    }

    // 从右向左扫描,找到最右边的有效算术表达式
    let endPos = text.length;
    
    // 从右向左找到第一个有效表达式字符的结束位置
    while (endPos > 0 && !this.validExprChars.has(text[endPos - 1])) {
      endPos--;
    }
    
    console.log(`[ArithmeticFilter] 有效字符结束位置: ${endPos}`);
    
    if (endPos === 0) {
      console.log(`[ArithmeticFilter] ❌ 未找到有效表达式字符`);
      return null;
    }
    
    // 从结束位置向左查找表达式的开始位置
    let startPos = endPos;
    while (startPos > 0 && this.validExprChars.has(text[startPos - 1])) {
      startPos--;
    }
    
    let expr = text.substring(startPos, endPos);
    console.log(`[ArithmeticFilter] 提取的原始表达式: "${expr}" (位置: ${startPos}-${endPos})`);

    // 清理表达式:移除前导的运算符和括号
    const cleanedExpr = expr.replace(/^[+\-*/()]+/, "");
    console.log(`[ArithmeticFilter] 清理后表达式: "${cleanedExpr}"`);
    expr = cleanedExpr;

    // 验证表达式是否包含运算符(不是单纯的数字)
    if (!this.hasOperatorPattern.test(expr)) {
      console.log(`[ArithmeticFilter] ❌ 表达式不包含运算符(纯数字)`);
      return null;
    }
    console.log(`[ArithmeticFilter] ✓ 包含运算符`);

    // 验证表达式的有效性
    if (!this.isValidExpression(expr)) {
      console.log(`[ArithmeticFilter] ❌ 表达式验证失败`);
      return null;
    }
    console.log(`[ArithmeticFilter] ✓ 表达式有效`);

    console.log(`[ArithmeticFilter] 最终提取的表达式: "${expr}"`);
    
    return {
      expr: expr,
      startPos: startPos,
      endPos: endPos
    };
  }

  /**
   * 验证表达式的基本有效性
   * @param {string} expr - 表达式
   * @returns {boolean} - 是否有效
   */
  isValidExpression(expr) {
    if (!expr || expr.length === 0) return false;

    // 检查括号是否匹配
    let parenthesesCount = 0;
    for (let char of expr) {
      if (char === "(") parenthesesCount++;
      if (char === ")") parenthesesCount--;
      if (parenthesesCount < 0) return false;
    }
    if (parenthesesCount !== 0) return false;

    // 检查是否以运算符结尾
    if (/[+\-*/]$/.test(expr)) return false;

    // 检查是否有连续的运算符(除了负号)
    if (/[+*/]{2,}/.test(expr)) return false;

    return true;
  }

  /**
   * 安全地计算表达式
   * @param {string} expr - 算术表达式
   * @returns {number|null} - 计算结果或null
   */
  safeEvaluate(expr) {
    console.log(`[ArithmeticFilter] --- safeEvaluate 开始 ---`);
    console.log(`[ArithmeticFilter] 计算表达式: "${expr}"`);

    try {
      const funcCode = '"use strict"; return (' + expr + ")";
      const result = Function(funcCode)();
      
      if (typeof result !== "number" || !isFinite(result)) {
        console.log(`[ArithmeticFilter] ❌ 结果不是有效数字`);
        return null;
      }

      console.log(`[ArithmeticFilter] ✓ 计算成功: ${result}`);
      return result;
    } catch (error) {
      console.log(`[ArithmeticFilter] ❌ 计算错误: ${error.message}`);
      return null;
    }
  }

  /**
   * 格式化数字结果
   * @param {number} num - 数字
   * @returns {string} - 格式化后的字符串
   */
  formatNumber(num) {
    if (Number.isInteger(num)) {
      return num.toString();
    }
    return num.toFixed(10).replace(/\.?0+$/, "");
  }

  /**
   * Filter主方法:处理候选项列表
   * @param {Array<Candidate>} candidates - 候选项数组
   * @param {Environment} env - 环境对象
   * @returns {Array<Candidate>} - 处理后的候选项数组
   */
  filter(candidates, env) {
    console.log(`\n========== [ArithmeticFilter] filter 开始 ==========`);
    console.log(`[ArithmeticFilter] 收到 ${candidates.length} 个候选项`);
    
    // 获取上下文
    const context = env.engine.context;
    if (!context) {
      console.log(`[ArithmeticFilter] ❌ context不存在`);
      console.log(`========== [ArithmeticFilter] filter 结束 ==========\n`);
      return candidates;
    }

    // 获取前置文本和当前输入
    const precedingText = context.externalPrecedingText || "";
    const input = context.input || "";
    
    console.log(`[ArithmeticFilter] 前置文本: "${precedingText}"`);
    console.log(`[ArithmeticFilter] 当前输入: "${input}"`);

    // 如果前置文本为空,不处理
    if (!precedingText) {
      console.log(`[ArithmeticFilter] 前置文本为空,跳过处理`);
      console.log(`========== [ArithmeticFilter] filter 结束 ==========\n`);
      return candidates;
    }

    // 组合完整文本
    const fullText = precedingText + input;
    console.log(`[ArithmeticFilter] 完整文本: "${fullText}"`);

    // 提取表达式
    const exprInfo = this.extractExpression(fullText);
    if (!exprInfo) {
      console.log(`[ArithmeticFilter] ❌ 未提取到有效表达式`);
      console.log(`========== [ArithmeticFilter] filter 结束 ==========\n`);
      return candidates;
    }

    const expression = exprInfo.expr;
    console.log(`[ArithmeticFilter] ✓ 识别到表达式: "${expression}"`);

    // 检查表达式是否主要在前置文本中
    const precedingTextLen = precedingText.length;
    if (exprInfo.startPos >= precedingTextLen) {
      // 表达式完全在当前输入中,让Translator处理
      console.log(`[ArithmeticFilter] 表达式完全在当前输入中,交由Translator处理`);
      console.log(`========== [ArithmeticFilter] filter 结束 ==========\n`);
      return candidates;
    }

    console.log(`[ArithmeticFilter] ✓ 表达式在前置文本中,由Filter处理`);

    // 计算结果
    const result = this.safeEvaluate(expression);
    if (result === null) {
      console.log(`[ArithmeticFilter] ❌ 计算失败`);
      console.log(`========== [ArithmeticFilter] filter 结束 ==========\n`);
      return candidates;
    }

    console.log(`[ArithmeticFilter] ✓ 计算结果: ${result}`);

    // 格式化结果
    const formattedResult = this.formatNumber(result);
    console.log(`[ArithmeticFilter] 格式化结果: "${formattedResult}"`);

    // 创建计算结果候选项
    const arithmeticCandidates = [];

    console.log(`[ArithmeticFilter] --- 生成候选项 ---`);

    // 候选项1: 只显示结果
    const cand1 = new Candidate(
      "arithmetic",
      0,
      input.length,
      formattedResult,
      `= ${expression}`
    );
    arithmeticCandidates.push(cand1);
    console.log(`[ArithmeticFilter] 添加候选项: "${formattedResult}" (= ${expression})`);

    // 候选项2: 显示完整等式
    const cand2 = new Candidate(
      "arithmetic",
      0,
      input.length,
      `${expression} = ${formattedResult}`,
      "算术计算"
    );
    arithmeticCandidates.push(cand2);
    console.log(`[ArithmeticFilter] 添加候选项: "${expression} = ${formattedResult}"`);

    // 候选项3: 只显示表达式
    const cand3 = new Candidate(
      "arithmetic",
      0,
      input.length,
      expression,
      "表达式"
    );
    arithmeticCandidates.push(cand3);
    console.log(`[ArithmeticFilter] 添加候选项: "${expression}"`);

    // 将算术候选项添加到原候选项列表的开头
    console.log(`[ArithmeticFilter] 总共生成 ${arithmeticCandidates.length} 个算术候选项`);
    console.log(`[ArithmeticFilter] 将算术候选项插入到列表开头`);
    
    const result_candidates = [...arithmeticCandidates, ...candidates];
    console.log(`[ArithmeticFilter] 最终候选项数量: ${result_candidates.length}`);
    console.log(`========== [ArithmeticFilter] filter 结束 (成功) ==========\n`);
    
    return result_candidates;
  }

  /**
   * 清理函数:插件卸载时调用
   */
  finalizer() {
    console.log("[ArithmeticFilter] 卸载算术表达式过滤器");
  }
}
