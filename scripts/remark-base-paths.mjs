// Root-relative links in Markdown/MDX are authored without the deployment prefix.
export default function basePaths() {
  return (tree) => {
    const walk = (node) => {
      if (
        ['link', 'image', 'definition'].includes(node.type) &&
        node.url?.startsWith('/') &&
        !node.url.startsWith('//') &&
        !/^\/Homepage(?:\/|$)/.test(node.url)
      ) {
        node.url = `/Homepage${node.url}`;
      }
      node.children?.forEach(walk);
    };
    walk(tree);
  };
}
