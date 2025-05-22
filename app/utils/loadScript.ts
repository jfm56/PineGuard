export class LoadScript {
  static load(src: string, id?: string): Promise<void> {
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
      if (id) { script.id = id; }
      script.src = src;
      script.async = true;
      script.defer = true;
      const timeoutId: NodeJS.Timeout = setTimeout(() => {
        script.remove();
        reject(new Error(`Timeout loading script: ${src}`));
      }, 10000); // 10 second timeout
      script.onload = (): void => {
        if (timeoutId) { clearTimeout(timeoutId); }
        
        resolve();
      };
      script.onerror = (): void => {
        if (timeoutId) { clearTimeout(timeoutId); }
        
        reject(new Error(`Failed to load script: ${src}`));
      };
      document.head.appendChild(script);
    });
  }
}

