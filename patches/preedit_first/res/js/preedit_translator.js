// preedit_translator.js
// 将当前的 preedit 内容作为一个候选项，并置顶。

export class PreeditTranslator {
  constructor(env) {
    // 初始化
  }

  translate(input, segment, env) {
    // 获取当前的 preedit 文本
    // env.engine.context.preedit 是一个 Preedit 对象，.text 获取其文本内容
    // 这里的 preedit 是整个输入缓冲区的显示文本（包含已确认但未上屏的段落）
    const preedit = env.engine.context.preedit.text;

    // 如果 preedit 为空，则不生成候选项
    if (!preedit) {
      return [];
    }

    // 创建候选项
    // type: 'preedit' (自定义类型)
    // start: segment.start
    // end: segment.end
    // text: preedit (显示的文本)
    // comment: '回显' (注释)
    // quality: 100000 (高权重，确保排在第一位)
    
    // 注意：如果当前有多个分词段落（例如“你”+“hao”），preedit 包含“你好”。
    // 当前 segment 对应“hao”。如果用“你好”替换“hao”，最终结果可能是“你你好”。
    // 这种行为符合“将 preedit 放入候选”的字面定义。
    const candidate = new Candidate(
      'preedit',
      segment.start,
      segment.end,
      preedit,
      'Preedit',
      100000
    );

    return [candidate];
  }
}
