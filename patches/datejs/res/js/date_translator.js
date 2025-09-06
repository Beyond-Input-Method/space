// 日期时间
// -------------------------------------------------------
// 使用 JavaScript 实现，适配 librime-qjs 插件系统。
// by @[HuangJian](https://github.com/HuangJian)

/** @type {Object.<string, string>} */
const keys = {}

/**
 * 日期时间翻译器
 * @implements {Translator}
 */
export class DateTranslator {
  /**
   * Initialize the date translator
   * @param {Environment} env - The Rime environment
   */
  constructor(env) {
    console.log(`date translator init`)

    const config = env.engine.schema.config
    const namespace = env.namespace
    keys.date = config.getString(namespace + '/date') || 'rq'
    keys.time = config.getString(namespace + '/time') || 'sj'
    keys.week = config.getString(namespace + '/week') || 'xq'
    keys.datetime = config.getString(namespace + '/datetime') || 'dt'
    keys.timestamp = config.getString(namespace + '/timestamp') || 'ts'
  }

  /**
   * Clean up the date translator
   */
  finalizer() {
    console.log(`date translator finit`)
  }

  /**
   * Translate date and time related input
   * @param {string} input - The input string to translate
   * @param {Segment} segment - The input segment
   * @param {Environment} env - The Rime environment
   * @returns {Array<Candidate>} Array of translation candidates
   */
  translate(input, segment, env) {
    const now = new Date()

    const candidates = []

    // 提高权重的原因：因为在方案中设置了大于 1 的 initial_quality，导致 rq sj xq dt ts 产出的候选项在所有词语的最后。
    const yieldCandidate = (text) =>
      candidates.push(new Candidate('date', segment.start, segment.end, text, '', 100))

    // 日期
    if (input === keys.date) {
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const date = String(now.getDate()).padStart(2, '0')

      yieldCandidate(`${year}-${month}-${date}`)
      yieldCandidate(`${year}/${month}/${date}`)
      yieldCandidate(`${year}.${month}.${date}`)
      yieldCandidate(`${year}${month}${date}`)
      yieldCandidate(`${year}年${Number(month)}月${Number(date)}日`)
    }
    // 时间
    else if (input === keys.time) {
      const hours = String(now.getHours()).padStart(2, '0')
      const minutes = String(now.getMinutes()).padStart(2, '0')
      const seconds = String(now.getSeconds()).padStart(2, '0')

      yieldCandidate(`${hours}:${minutes}`)
      yieldCandidate(`${hours}:${minutes}:${seconds}`)
      yieldCandidate(`${hours}${minutes}${seconds}`)
    }
    // 星期
    else if (input === keys.week) {
      const weekTable = ['日', '一', '二', '三', '四', '五', '六']
      const weekDay = weekTable[now.getDay()]

      yieldCandidate('星期' + weekDay)
      yieldCandidate('礼拜' + weekDay)
      yieldCandidate('周' + weekDay)
    }
    // ISO 8601/RFC 3339 的时间格式 （固定东八区）（示例 2022-01-07T20:42:51+08:00）
    else if (input === keys.datetime) {
      const offset = '+08:00'
      const isoDate = now.toISOString().slice(0, 19)
      yieldCandidate(isoDate + offset)

      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const hours = String(now.getHours()).padStart(2, '0')
      const minutes = String(now.getMinutes()).padStart(2, '0')
      const seconds = String(now.getSeconds()).padStart(2, '0')

      yieldCandidate(`${year}-${month}-${day} ${hours}:${minutes}:${seconds}`)
      yieldCandidate(`${year}${month}${day}${hours}${minutes}${seconds}`)
    }
    // 时间戳（十位数，到秒，示例 1650861664）
    else if (input === keys.timestamp) {
      yieldCandidate(Math.floor(now.getTime() / 1000).toString())
    }

    return candidates
  }
}
