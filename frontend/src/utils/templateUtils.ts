export function replaceVariables(content: string, variables: Record<string, string>): string {
  return content.replace(/\{\{([^}]+)\}\}/g, (match, varName) => {
    const trimmedVarName = varName.trim();
    return variables[trimmedVarName] !== undefined ? variables[trimmedVarName] : match;
  });
}