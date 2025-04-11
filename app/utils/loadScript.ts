export function loadScript(src: string, id?: string): Promise<void> {
  // Check if the script is already loaded
  if (id && document.getElementById(id)) {
    return Promise.resolve();
  }

  const existingScript = document.querySelector(`script[src="${src}"]`);
  if (existingScript) {
    return Promise.resolve();
  }
  return new Promise((resolve, reject) => {


    const script = document.createElement('script');
    if (id) {script.id = id;}
    script.src = src;
    script.async = true;
    script.defer = true;
    
    let timeoutId: NodeJS.Timeout;

    script.onload = () => {
      if (timeoutId) {clearTimeout(timeoutId);}
      console.log(`Script loaded successfully: ${src}`);
      resolve();
    };
    
    script.onerror = (err) => {
      if (timeoutId) {clearTimeout(timeoutId);}
      console.error(`Error loading script ${src}:`, err);
      reject(new Error(`Failed to load script: ${src}`));
    };

    // Add a timeout to prevent hanging
    timeoutId = setTimeout(() => {
      script.remove();
      reject(new Error(`Timeout loading script: ${src}`));
    }, 10000); // 10 second timeout
    
    document.head.appendChild(script);
  });
}
