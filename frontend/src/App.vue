<template>
  <div id="app" class="app-container">
    <ErrorBoundary>
      <router-view></router-view>
    </ErrorBoundary>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from "vue";
import ErrorBoundary from "@/components/ErrorBoundary.vue";

let app: HTMLElement | null = null;
const handleMouseMove = (e: MouseEvent) => {
  const x = e.clientX / window.innerWidth;
  const y = e.clientY / window.innerHeight;
  app?.style.setProperty("--mouse-x", `${x}`);
  app?.style.setProperty("--mouse-y", `${y}`);
};

onMounted(() => {
  // 添加动态背景动画
  app = document.querySelector(".app-container");
  app?.addEventListener("mousemove", handleMouseMove);
});

onUnmounted(() => {
  // 移除事件监听器，防止内存泄漏
  app?.removeEventListener("mousemove", handleMouseMove);
});
</script>

<style>
@import "@/styles/tech-theme.scss";

#app {
  height: 100vh;
  background: var(--bg-dark);
  position: relative;
  overflow: hidden;
}

.app-container {
  height: 100vh;
  position: relative;
}

.app-container::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
    circle at calc(var(--mouse-x, 0.5) * 100%) calc(var(--mouse-y, 0.5) * 100%),
    rgba(14, 165, 233, 0.15),
    transparent 25%
  );
  pointer-events: none;
  transition: all 0.3s ease;
  z-index: 0;
}

.app-container::after {
  content: "";
  position: fixed;
  top: -50%;
  left: -50%;
  right: -50%;
  bottom: -50%;
  width: 200%;
  height: 200%;
  background: transparent;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%239C92AC' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  z-index: -1;
  animation: grain 8s steps(10) infinite;
  opacity: 0.5;
  pointer-events: none;
}

@keyframes grain {
  0%,
  100% {
    transform: translate(0, 0);
  }
  10% {
    transform: translate(-5%, -10%);
  }
  20% {
    transform: translate(-15%, 5%);
  }
  30% {
    transform: translate(7%, -25%);
  }
  40% {
    transform: translate(-5%, 25%);
  }
  50% {
    transform: translate(-15%, 10%);
  }
  60% {
    transform: translate(15%, 0%);
  }
  70% {
    transform: translate(0%, 15%);
  }
  80% {
    transform: translate(3%, 35%);
  }
  90% {
    transform: translate(-10%, 10%);
  }
}
</style>
