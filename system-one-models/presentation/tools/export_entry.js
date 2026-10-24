import { exportToSvg } from "@excalidraw/excalidraw";
window.__exportFrame = async (scene, frameId, files) => {
  const frame = scene.elements.find((e) => e.id === frameId);
  const svg = await exportToSvg({
    elements: scene.elements, files: files || {},
    appState: { exportBackground: true, viewBackgroundColor: "#ffffff", exportWithDarkMode: false },
    exportPadding: 0, exportingFrame: frame,
  });
  return new XMLSerializer().serializeToString(svg);
};
window.__ready = true;
