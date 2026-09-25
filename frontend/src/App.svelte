<script>
  let username = 'processor'
  let password = 'herb123456'
  let token = localStorage.getItem('herb_token') || ''
  let role = localStorage.getItem('herb_role') || ''
  let rows = []
  let herb = '白芍'
  let tempC = 110
  let minutes = 10
  let error = ''
  let banner = ''
  let canSubmit = false

  async function api(path, options = {}) {
    const res = await fetch(path, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    })
    const data = await res.json().catch(() => ({}))
    if (!res.ok) throw new Error(data.detail || '请求失败')
    return data
  }

  async function enter() {
    const data = await api('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    })
    token = data.access_token
    role = data.role
    localStorage.setItem('herb_token', token)
    localStorage.setItem('herb_role', role)
    await init()
  }

  async function init() {
    // 入口是否可提交以后端按真实角色返回的结果为准，质检默认不可提交
    const hint = await api('/api/auth/submit-hint')
    canSubmit = hint.can_submit
    await load()
  }

  async function load() {
    rows = await api('/api/batches')
  }

  async function save() {
    error = ''
    banner = ''
    try {
      await api('/api/batches', {
        method: 'POST',
        body: JSON.stringify({
          herb,
          steps: [{ name: '清炒', temp_c: Number(tempC), minutes: Number(minutes) }],
        }),
      })
      // 只有真正写库成功才提示已保存，新行以后端返回的数据为准
      banner = '已保存'
      await load()
    } catch (err) {
      // 失败只保留原因：不提示已保存、不插入空行、库行保持原数
      banner = ''
      error = err.message
    }
  }

  function leave() {
    localStorage.clear()
    token = ''
    role = ''
  }

  // canSubmit 默认 false：带旧 token 进入也要等后端按真实角色判定，质检不会闪现可提交入口
  if (token) init()
</script>

<main>
  <h1>饮片炮制记录台</h1>
  {#if !token}
    <p>炮制记录整包保存。清炒温度须在 80 到 150，时长须在 5 到 30 分钟。</p>
    <input bind:value={username} />
    <input type="password" bind:value={password} />
    <button on:click={enter}>登录</button>
    <p>processor / herb123456 可写；checker / check123456 只读</p>
  {:else}
    <p>
      <button on:click={leave}>退出</button>
    </p>
    {#if canSubmit}
      <input bind:value={herb} placeholder="饮片" />
      <input type="number" bind:value={tempC} />
      <input type="number" bind:value={minutes} />
      <button on:click={save}>写入清炒记录</button>
      {#if error}<p>{error}</p>{/if}
      {#if banner}<p>{banner}</p>{/if}
    {/if}
    <ul>
      {#each rows as row}
        <li>{row.herb} · {row.verdict} · {row.reason} · 温度 {row.doc.steps[0].temp_c}</li>
      {/each}
    </ul>
  {/if}
</main>

<style>
  main { font-family: sans-serif; max-width: 720px; margin: 24px auto; color: #3f2f1f; }
  h1 { color: #7c2d12; }
  input { margin-right: 8px; padding: 6px; }
</style>
