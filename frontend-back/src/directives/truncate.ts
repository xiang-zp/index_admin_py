import type { Directive, DirectiveBinding } from 'vue'

interface TruncateElement extends HTMLElement {
  _checkTruncation?: () => void
}

export const vTruncate: Directive = {
  mounted(el: TruncateElement, binding: DirectiveBinding) {
    const checkTruncation = () => {
      // 检查是否被截断的逻辑：
      // scrollHeight > clientHeight 表示内容高度超过了容器高度
      // 或者 scrollWidth > clientWidth 表示内容宽度超过了容器宽度（单行情况）
      const isTruncated = el.scrollHeight > el.clientHeight || el.scrollWidth > el.clientWidth
      
      // 将检测结果传递给回调函数
      if (binding.value && typeof binding.value === 'function') {
        binding.value(isTruncated)
      }
    }

    // 保存引用以便清理
    el._checkTruncation = checkTruncation
    
    // 初始检查
    // 使用 requestAnimationFrame 确保在渲染后检查
    requestAnimationFrame(checkTruncation)
    
    // 监听窗口大小变化
    window.addEventListener('resize', checkTruncation)
  },
  
  updated(el: TruncateElement, _binding: DirectiveBinding) {
    // 数据更新时重新检查
    if (el._checkTruncation) {
      requestAnimationFrame(el._checkTruncation)
    }
  },
  
  unmounted(el: TruncateElement) {
    if (el._checkTruncation) {
      window.removeEventListener('resize', el._checkTruncation)
      delete el._checkTruncation
    }
  }
}
