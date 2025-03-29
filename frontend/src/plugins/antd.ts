import { App } from "vue";
import {
  Button,
  Select,
  Form,
  Input,
  Tag,
  Radio,
  Empty,
  Spin,
  Tooltip,
  message,
  Card,
  Row,
  Col,
  Table,
  Modal,
} from "ant-design-vue";
// 导入所有组件样式
import "ant-design-vue/dist/reset.css";

export function setupAntd(app: App<Element>) {
  app.use(Button);
  app.use(Select);
  app.use(Form);
  app.use(Input);
  app.use(Tag);
  app.use(Radio);
  app.use(Empty);
  app.use(Spin);
  app.use(Tooltip);
  app.use(Card);
  app.use(Row);
  app.use(Col);
  app.use(Table);
  app.use(Modal);

  // 配置全局消息
  app.config.globalProperties.$message = message;
}
