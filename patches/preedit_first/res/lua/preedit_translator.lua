-- preedit_translator.lua
-- 将当前的 preedit 内容作为一个候选项，并置顶。

local function yield_cand(seg, text, comment, quality)
    local cand = Candidate('preedit', seg.start, seg._end, text, comment or '')
    cand.quality = quality or 100000
    yield(cand)
end

local M = {}

function M.init(env)
    -- 初始化
    env.name_space = env.name_space:gsub('^*', '')
end

function M.func(input, seg, env)
    -- 获取当前的 preedit 文本
    local context = env.engine.context
    if not context then
        return
    end
    
    -- 使用 context:get_preedit() 获取 Preedit 对象，然后通过 .text 获取文本
    local preedit_obj = context:get_preedit()
    if not preedit_obj then
        return
    end
    
    local preedit = preedit_obj.text
    
    -- 如果 preedit 为空，则不生成候选项
    if not preedit or preedit == '' then
        return
    end
    
    -- 创建候选项
    -- type: 'preedit' (自定义类型)
    -- start: seg.start
    -- end: seg._end
    -- text: preedit (显示的文本)
    -- comment: 'Preedit' (注释)
    -- quality: 100000 (高权重，确保排在第一位)
    
    -- 注意：如果当前有多个分词段落（例如"你"+"hao"），preedit 包含"你好"。
    -- 当前 segment 对应"hao"。如果用"你好"替换"hao"，最终结果可能是"你你好"。
    -- 这种行为符合"将 preedit 放入候选"的字面定义。
    yield_cand(seg, preedit, '', 100000)
end

return M
