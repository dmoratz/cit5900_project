# Import libraries
import simpy
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Track wait times at each stage
wait_times = []

def research_paper(env, paper_id, editors, peer_reviewers, authors):
    """
    Simulate the process that a single research paper will go through:
    Inital Review, Peer Review, and Revision before getting published

    Parameters:
    - env: SimPy environment
    - paper_id: the id for research paper
    - editors: Resource of editors
    - peer_reviewer: Resource of peer reviewers
    - authors: Resource of authors
    """
    # Get the submission time
    submission_time = env.now
    
    # Initial review process
    with editors.request() as req:
        # Wait for available editor
        yield req
        # Save the wait time for the editor in wait_times
        wait_times.append(('editor_wait', env.now - submission_time))

        # Assume initial review takes average of 5 days
        editor_time = random.expovariate(1.0/5)
        yield env.timeout(editor_time)
        
        # Assume there is 30% chance to be rejected by editor
        if random.random() < 0.3:
            # Save the time for the editor to reject
            wait_times.append(('editor_reject', env.now - submission_time))
            return
    
    # Mark the time that editor finished the initial reviews
    editor_done_time = env.now
    
    # Peer review process
    with peer_reviewers.request() as req:
        # Wait for available peer reviewer
        yield req
        # Save the wait time for the peer reviewer in wait_times
        wait_times.append(('peer_reviewer_wait', env.now - editor_done_time))
        
        # Assume peer review takes average of 7 days
        review_time = random.expovariate(1.0/7)
        yield env.timeout(review_time)
        
        # Assume there is 30% chance of being reject by peer reviewer
        if random.random() < 0.3:
            # Save the time for the peer reviewer to reject
            wait_times.append(('peer_reviewer_reject', env.now - submission_time))
            return
    
    # Mark the time that peer reviewer finished peer reviews
    peer_reviewer_done_time = env.now
    
    # Revision Process
    # Assume that a reasearch papaer could go through revision at most three times
    revision_rounds = 0
    max_revisions = 3

    # Assume that there is 50% of chance that the paper needs another round of revision
    while revision_rounds < max_revisions and random.random() < 0.5:

        # Keep track of the revision rounds
        revision_rounds += 1
        
        with authors.request() as req:
            # Wait for available author
            yield req
            
            # Assume it takes average of 7 days for revision
            revision_time = random.expovariate(1.0/7)
            yield env.timeout(revision_time)
        
        # Mark the time when author finished revision
        revision_done_time = env.now
        
        # Reviewer check for revisions
        with peer_reviewers.request() as req:
            # Wait for available peer reviewer
            yield req
            # Save the time wait for peer reviewer
            wait_times.append(('revision_reviewer_wait', env.now - revision_done_time))
            
            # Assume it takes average of 5 days to check for the revision
            revision_review_time = random.expovariate(1.0/5)
            yield env.timeout(revision_review_time)
        
        # Mark the time that peer reviewer finished checking revision
        review_done_time = env.now
    
    # Save the time it takes for a research paper to be published
    wait_times.append(('published', env.now - submission_time))

def paper_generator(env, editors, peer_reviewers, authors, submission_frequency):
    """
    Generates paper submissions at a given rate

    Parameters:
    - env: SimPy environment
    - editors: Resource of editors
    - peer_reviewer: Resource of peer reviewers
    - authors: Resource of authors
    - submission_frequency: Submission frequency for paper submisson
    """
    # Keep track of the paper id 
    paper_id = 0
    while True:
        paper_id += 1
        yield env.timeout(random.expovariate(1/submission_frequency))
        # Process the research paper
        env.process(research_paper(env, f"Paper {paper_id}", editors, peer_reviewers, authors))

def analyze_results(wait_times, sim_time):
    """
    Analyze the simulation results with statistics
    """
    try:
        # Organize wait times by type, save it in the dictionary
        wait_times_dict = defaultdict(list)
        for wait_type, time in wait_times:
            wait_times_dict[wait_type].append(time)
        
        # Calculate statistics for different type of wait time
        stats = {}
        for wait_type, time in wait_times_dict.items():
            stats[wait_type] = {
                'count': len(time),
                'mean': np.mean(time) if time else 0,
                'median': np.median(time) if time else 0,
                'min': min(time) if time else 0,
                'max': max(time) if time else 0
            }
        
        # Print summary statistics
        print(f"Simulation completed over {sim_time} days")
        total_paper_submissions = sum(len(wait_times_dict[t]) for t in ['published', 'editor_reject', 'peer_reviewer_reject'])
        print(f"Total paper submissions: {total_paper_submissions}")
        print(f"Papers published: {len(wait_times_dict['published'])} ({len(wait_times_dict['published'])/total_paper_submissions:.2%})")
        print(f"Papers rejected during initial review: {len(wait_times_dict['editor_reject'])}")
        print(f"Papers rejected during peer review: {len(wait_times_dict['peer_reviewer_reject'])}")
        print("\nWait time statistics (in days):")
        for wait_type in ["editor_wait", "peer_reviewer_wait",
                        "revision_reviewer_wait", "editor_reject", 
                        "peer_reviewer_reject", "published"]:
            if wait_type in ["published", "editor_reject", "peer_reviewer_reject"]:
                print(f"  Total time for {wait_type} papers: {stats[wait_type]['mean']:.2f} days (average)")
            else:
                print(f"  {wait_type}: {stats[wait_type]['mean']:.2f} days (average)")
    except Exception as e:
        print(f"An error occurred while analyzing the result: {str(e)}")

def run_simulation(sim_time=365, submission_frequency=3, editors_capacity=2):
    """
    Run the simulation for the specified time

    Parameters:
    - sim_time: simulation time in terms of days
    - submission_frequency: frequency for paper submission
    - editors_capacity: number of editors available
    """
    # reset wait times
    wait_times.clear()
    
    # Create SimPy environment
    env = simpy.Environment()
    
    # Create resources
    editors = simpy.Resource(env, capacity=editors_capacity)
    peer_reviewers = simpy.Resource(env, capacity=5)
    authors = simpy.Resource(env, capacity=float('inf'))
    
    # Start paper generation process
    env.process(paper_generator(env, editors, peer_reviewers, authors, submission_frequency))
    
    # Run simulation
    env.run(until=sim_time)
    
    # Analyze the simulation results
    analyze_results(wait_times, sim_time)

def part4_des_pipeline():
    """
    Function to complete Part 4 DES completely
    """
    # Run the simulation
    run_simulation()

    # What-if scenario: More editors available
    print("\n--- What-if Scenario: More Available Editors ---")
    # Increase number of editors from 2 to 3
    run_simulation(editors_capacity=3)
