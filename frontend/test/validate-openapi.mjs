import SwaggerParser from '@apidevtools/swagger-parser';
import { fileURLToPath } from 'node:url';

const api = await SwaggerParser.validate(fileURLToPath(new URL('../../openapi.yaml', import.meta.url)));
const methods = Object.values(api.paths).flatMap(path => Object.keys(path).filter(method => ['get', 'post', 'patch', 'delete'].includes(method)));
if (methods.length < 17) throw new Error(`Expected the complete service contract, found ${methods.length} operations.`);
console.log(`OpenAPI valid: ${methods.length} operations.`);
