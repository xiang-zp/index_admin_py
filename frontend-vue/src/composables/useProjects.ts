import { ref, onMounted, watch } from 'vue';
import * as projects from '@/services/projects';

export function useProjects(category?: string) {
  const projectsList = ref<projects.Project[]>([]);
  const categories = ref<projects.Category[]>([]);
  const loading = ref(true);
  const error = ref<string | null>(null);

  const loadData = async () => {
    try {
      loading.value = true;
      const [projectsData, categoriesData] = await Promise.all([
        projects.getProjects({ category }),
        projects.getProjectCategories()
      ]);
      projectsList.value = projectsData.items;
      categories.value = categoriesData;
      error.value = null;
    } catch (err) {
      error.value = err instanceof Error ? err.message : '加载失败';
      projectsList.value = [
        {
          id: 1,
          category: 'Python编程',
          title: 'Python基础语法精讲',
          description: '深入理解Python基础语法，包括变量、数据类型、控制流和函数等核心概念，为后续学习打下坚实基础。',
          date: '2024-02-15',
          color: 'bg-blue-100 text-blue-800'
        },
        {
          id: 2,
          category: 'Python编程',
          title: 'Python面向对象编程',
          description: '掌握Python面向对象编程思想，学习类、对象、继承、多态等重要概念，提升代码复用性和可维护性。',
          date: '2024-02-14',
          color: 'bg-blue-100 text-blue-800'
        },
        {
          id: 3,
          category: 'Python自动化',
          title: 'Python自动化办公实战',
          description: '使用Python自动化处理Excel、Word、PDF等办公文档，提升工作效率，实现批量数据处理和报表生成。',
          date: '2024-02-13',
          color: 'bg-purple-100 text-purple-800'
        },
        {
          id: 4,
          category: 'Python自动化',
          title: 'Python爬虫入门与实践',
          description: '学习Python爬虫技术，掌握requests、BeautifulSoup等库的使用，实现数据采集和网页抓取功能。',
          date: '2024-02-12',
          color: 'bg-purple-100 text-purple-800'
        },
        {
          id: 5,
          category: '测试工具',
          title: 'Selenium自动化测试',
          description: '深入学习Selenium自动化测试框架，掌握元素定位、页面对象模型等技巧，实现Web应用自动化测试。',
          date: '2024-02-11',
          color: 'bg-green-100 text-green-800'
        },
        {
          id: 6,
          category: '测试工具',
          title: 'JMeter性能测试实战',
          description: '学习JMeter性能测试工具，掌握压测场景设计、脚本录制和结果分析，提升系统性能测试能力。',
          date: '2024-02-10',
          color: 'bg-green-100 text-green-800'
        },
        {
          id: 7,
          category: '测试基础',
          title: '软件测试基础理论',
          description: '系统学习软件测试理论基础，包括测试类型、测试方法、测试流程和测试用例设计等核心知识。',
          date: '2024-02-09',
          color: 'bg-orange-100 text-orange-800'
        },
        {
          id: 8,
          category: '测试基础',
          title: '黑盒测试与白盒测试',
          description: '深入理解黑盒测试和白盒测试的区别与应用场景，掌握等价类划分、边界值分析等测试用例设计方法。',
          date: '2024-02-08',
          color: 'bg-orange-100 text-orange-800'
        },
        {
          id: 9,
          category: '测试开发',
          title: 'Python测试框架Pytest',
          description: '学习Pytest测试框架的使用，掌握fixture、参数化、mock等高级特性，构建高效的自动化测试体系。',
          date: '2024-02-07',
          color: 'bg-pink-100 text-pink-800'
        },
        {
          id: 10,
          category: '测试开发',
          title: '测试平台开发实战',
          description: '从零开始搭建测试平台，学习测试用例管理、执行调度、报告生成等功能开发，提升测试工程化能力。',
          date: '2024-02-06',
          color: 'bg-pink-100 text-pink-800'
        }
      ];
      categories.value = [
        { id: 'python', name: 'Python编程' },
        { id: 'automation', name: 'Python自动化' },
        { id: 'test-tool', name: '测试工具' },
        { id: 'test-basic', name: '测试基础' },
        { id: 'test-dev', name: '测试开发' }
      ];
    } finally {
      loading.value = false;
    }
  };

  onMounted(() => {
    loadData();
  });

  if (category) {
    watch(() => category, () => {
      loadData();
    });
  }

  return { projects: projectsList, categories, loading, error };
}
