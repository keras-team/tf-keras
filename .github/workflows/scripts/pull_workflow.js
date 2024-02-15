
/**
 * @license
 * Copyright 2023 Google LLC. All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =============================================================================
 */
/**
  Automatically recognize the event and add/remove labels accordingly.
    * For open events: Add a "size" label to provide additional information PR.
    * For synchronized events: Remove the "awaiting review" label to indicate
  that the event is no longer pending review.
    * For review request events: Add the "awaiting review" label to indicate
  that the PR requires review.
    * For closed events: Remove the "awaiting review" label as it is no longer
  applicable.
  @param {!object}
    GitHub objects can call GitHub APIs using their built-in library functions.
    The context object contains issue and PR details.
  @return {!object}
*/
module.exports = async ({github, context}) => {
  console.log('Processing pull request number: ', context.issue.number);
  if (context.payload.action == 'opened') {
    console.log('Trigger Event: ', context.payload.action);
    const size = context.payload.pull_request.additions +
        context.payload.pull_request.deletions;
    let labelsToAdd = '';
    if (size < 9) {
      labelsToAdd = 'size:XS';
    } else if (size < 49) {
      labelsToAdd = 'size:S';
    } else if (size < 249) {
      labelsToAdd = 'size:M';
    } else if (size < 999) {
      labelsToAdd = 'size:L';
    } else {
      labelsToAdd = 'size:XL';
    }
    console.log('Applying size label : ', labelsToAdd);
    return github.rest.issues.addLabels({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: context.issue.number,
      labels: [labelsToAdd],
    });
  } else if (context.payload.action == 'synchronize') {
    console.log('Trigger Event: ', context.payload.action);
    console.log(
        'Github event: pull_request updated with new code for PR number = ',
        context.issue.number);
    const labelsToRemove = 'ready to pull';
    let result;
    try {
    result = await github.rest.issues.removeLabel({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: context.issue.number,
      name: labelsToRemove,
    });
    console.log(`'${labelsToRemove}' label removed successfully.\n`);
    }
    catch(e){
       console.log(`'${labelsToRemove}' label dosen't exist in the PR. \n`);
       result = `'${labelsToRemove}' label dosen't exist in the PR.`;
    }
    return result;
  } else if (context.payload.action == 'closed') {
    console.log('Trigger Event: ', context.payload.action);
    console.log(
        'Github event: pull_request updated with new code for PR number =',
        context.payload.pull_request.number);
    const labelsToRemove = ['keras-team-review-pending','ready to pull'];
    let result = [];
    for(let label of labelsToRemove){
      try {
     let response = await github.rest.issues.removeLabel({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: context.issue.number,
      name: label,
    });
        result.push(response);
     }
      catch(e){
          console.log(`'${label}' label dosen't exist in the PR. \n`);
          result.push( `'${label}' label dosen't exist in the PR.`);
      }
    }
    return result;
  }
};